"""FastAPI application for market prediction"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from models import MarketSignal, MarketOverview, SentimentData, HistoricalPrice, ForecastResult
from services import (
    get_market_signals,
    get_sentiment_by_symbol,
    get_historical_prices,
    get_market_overview,
)

app = FastAPI(
    title="Market Prediction API",
    version="0.1.0",
    description="Predictive analytics platform for financial markets",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "market-api", "version": "0.1.0"}


@app.get("/api/v1/market/overview", response_model=MarketOverview)
async def market_overview():
    """Get high-level market overview"""
    data = get_market_overview()
    return MarketOverview(**data)


@app.get("/api/v1/market/signals", response_model=List[MarketSignal])
async def market_signals():
    """Get latest market signals with buy/sell/hold recommendations"""
    signals = get_market_signals()
    return [MarketSignal(**signal) for signal in signals]


@app.get("/api/v1/market/sentiment/{symbol}", response_model=SentimentData)
async def market_sentiment(symbol: str):
    """Get sentiment data for a specific symbol"""
    data = get_sentiment_by_symbol(symbol)
    return SentimentData(**data)


@app.get("/api/v1/market/historical/{symbol}", response_model=HistoricalPrice)
async def historical_data(symbol: str, days: int = 30):
    """Get historical price data for a symbol"""
    if days < 1 or days > 365:
        return {"error": "Days must be between 1 and 365"}
    data = get_historical_prices(symbol, days)
    return HistoricalPrice(**data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
