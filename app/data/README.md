import os
from datetime import datetime
from typing import Any, Dict

import psycopg2
from elasticsearch import Elasticsearch
from pymongo import MongoClient

from app.data.config import CONFIG


class DataIngestionService:
    def __init__(self):
        self.pg_conn = psycopg2.connect(
            host=CONFIG.pg_host,
            dbname=CONFIG.pg_db,
            user=CONFIG.pg_user,
            password=CONFIG.pg_password,
        )
        self.es = Elasticsearch(CONFIG.es_host)
        self.mongo_client = MongoClient(CONFIG.mongo_uri)
        self.mongo_db = self.mongo_client[CONFIG.mongo_db]

    def create_asset(self, symbol: str, name: str, asset_type: str = "stock", exchange: str = "NASDAQ") -> str:
        with self.pg_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO assets (symbol, name, asset_type, exchange)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (symbol) DO UPDATE SET name = EXCLUDED.name
                RETURNING id
                """,
                (symbol, name, asset_type, exchange),
            )
            asset_id = cur.fetchone()[0]
            self.pg_conn.commit()
            return str(asset_id)

    def get_asset_id(self, symbol: str):
        with self.pg_conn.cursor() as cur:
            cur.execute("SELECT id FROM assets WHERE symbol = %s", (symbol,))
            row = cur.fetchone()
            return str(row[0]) if row else None

    def ingest_price_snapshot(self, symbol: str, payload: Dict[str, Any]) -> None:
        asset_id = self.get_asset_id(symbol)
        if not asset_id:
            asset_id = self.create_asset(symbol, symbol)

        with self.pg_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO market_prices (
                    asset_id, ts, open_price, high_price, low_price, close_price, volume, source
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (asset_id, ts) DO NOTHING
                """,
                (
                    asset_id,
                    payload["ts"],
                    payload["open"],
                    payload["high"],
                    payload["low"],
                    payload["close"],
                    payload["volume"],
                    payload.get("source", "market_feed"),
                ),
            )
            self.pg_conn.commit()

    def ingest_news_item(self, asset_symbol: str, payload: Dict[str, Any]) -> None:
        self.mongo_db["news"].insert_one(
            {
                "asset_symbol": asset_symbol,
                "source": payload.get("source", "unknown"),
                "title": payload.get("title"),
                "content": payload.get("content"),
                "published_at": payload.get("published_at", datetime.utcnow().isoformat()),
                "raw": payload,
            }
        )

        self.es.index(
            index=CONFIG.es_index,
            document={
                "asset_symbol": asset_symbol,
                "title": payload.get("title", ""),
                "content": payload.get("content", ""),
                "source": payload.get("source", "unknown"),
                "published_at": payload.get("published_at", datetime.utcnow().isoformat()),
                "sentiment_score": payload.get("sentiment_score", 0.5),
                "sentiment_label": payload.get("sentiment_label", "neutral"),
                "url": payload.get("url", ""),
                "language": payload.get("language", "en"),
            },
        )

    def seed_sample_assets(self) -> None:
        for symbol, name in {
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft",
            "NVDA": "NVIDIA",
            "TSLA": "Tesla",
        }.items():
            self.create_asset(symbol, name)


def get_ingestion_service() -> DataIngestionService:
    return DataIngestionService()


if __name__ == "__main__":
    service = get_ingestion_service()
    service.seed_sample_assets()
    print("Data ingestion service initialized.")
