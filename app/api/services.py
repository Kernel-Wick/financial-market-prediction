"""Service layer for data retrieval and business logic"""

from typing import List, Dict
from datetime import datetime, timedelta
from models import MarketSignal, SentimentData, HistoricalPrice


def get_market_signals() -> List[Dict]:
    """Get latest market signals with buy/sell/hold recommendations"""
    return [
        {
            "symbol": "AAPL",
            "signal": "buy",
            "confidence": 0.82,
            "price": 218.45,
            "sentiment_score": 0.74,
        },
        {
            "symbol": "MSFT",
            "signal": "hold",
            "confidence": 0.79,
            "price": 432.12,
            "sentiment_score": 0.68,
        },
        {
            "symbol": "NVDA",
            "signal": "buy",
            "confidence": 0.88,
            "price": 122.81,
            "sentiment_score": 0.81,
        },
        {
            "symbol": "TSLA",
            "signal": "sell",
            "confidence": 0.71,
            "price": 242.50,
            "sentiment_score": 0.45,
        },
    ]


def get_sentiment_by_symbol(symbol: str) -> Dict:
    """Get sentiment data for a specific symbol"""
    sentiment_map = {
        "AAPL": {"sentiment_score": 0.74, "sentiment_label": "positive"},
        "MSFT": {"sentiment_score": 0.68, "sentiment_label": "positive"},
        "NVDA": {"sentiment_score": 0.81, "sentiment_label": "positive"},
        "TSLA": {"sentiment_score": 0.45, "sentiment_label": "neutral"},
    }
    data = sentiment_map.get(
        symbol.upper(), {"sentiment_score": 0.50, "sentiment_label": "neutral"}
    )
    return {
        "symbol": symbol.upper(),
        **data,
        "source": "aggregated",
    }


def get_historical_prices(symbol: str, days: int = 30) -> Dict:
    """Get historical price data for a symbol"""
    base_prices = {"AAPL": 200, "MSFT": 400, "NVDA": 100, "TSLA": 230}
    base_price = base_prices.get(symbol.upper(), 150)

    prices = []
    dates = []
    for i in range(days):
        prices.append(round(base_price + (i * 0.5) + (i % 3 - 1), 2))
        date = (datetime.utcnow() - timedelta(days=days - i)).strftime("%Y-%m-%d")
        dates.append(date)

    return {
        "symbol": symbol.upper(),
        "prices": prices,
        "dates": dates,
    }


def get_market_overview() -> Dict:
    """Get high-level market overview"""
    signals = get_market_signals()
    return {
        "total_symbols": len(signals),
        "active_signals": len([s for s in signals if s["signal"] != "hold"]),
        "market_status": "bullish",
    }
