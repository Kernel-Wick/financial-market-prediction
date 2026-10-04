from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MarketSignal(BaseModel):
    """Market signal with price and sentiment data"""
    symbol: str = Field(..., description="Stock/asset symbol")
    signal: str = Field(..., description="buy, sell, or hold")
    confidence: float = Field(..., ge=0, le=1, description="Confidence 0-1")
    price: float = Field(..., gt=0, description="Current price")
    sentiment_score: float = Field(..., ge=0, le=1, description="Sentiment 0-1")


class MarketOverview(BaseModel):
    """High-level market overview"""
    total_symbols: int
    active_signals: int
    market_status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SentimentData(BaseModel):
    """Sentiment analysis result"""
    symbol: str
    sentiment_score: float = Field(..., ge=0, le=1)
    sentiment_label: str
    source: str = "aggregated"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HistoricalPrice(BaseModel):
    """Historical price data"""
    symbol: str
    prices: List[float]
    dates: List[str]
    timestamps: Optional[List[datetime]] = None


class ForecastResult(BaseModel):
    """Forecast prediction result"""
    symbol: str
    forecasted_prices: List[float]
    confidence_scores: List[float]
    model_version: str = "baseline_v0.1"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
