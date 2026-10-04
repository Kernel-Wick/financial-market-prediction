import os
from dataclasses import dataclass


@dataclass
class DataLayerConfig:
    pg_host: str = os.getenv("PG_HOST", "localhost")
    pg_db: str = os.getenv("PG_DB", "marketdb")
    pg_user: str = os.getenv("PG_USER", "postgres")
    pg_password: str = os.getenv("PG_PASSWORD", "postgres")

    es_host: str = os.getenv("ES_HOST", "http://localhost:9200")
    es_index: str = os.getenv("ES_INDEX", "market-news")

    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db: str = os.getenv("MONGO_DB", "market_data")


CONFIG = DataLayerConfig()
