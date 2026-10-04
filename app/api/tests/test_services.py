"""Tests for service layer"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from services import (
    get_market_signals,
    get_sentiment_by_symbol,
    get_historical_prices,
    get_market_overview,
)


class TestServices:
    def test_get_market_signals(self):
        """Test market signals service"""
        signals = get_market_signals()
        assert len(signals) >= 1
        assert signals[0]["symbol"] == "AAPL"
        assert signals[0]["signal"] in ["buy", "sell", "hold"]

    def test_get_sentiment_by_symbol(self):
        """Test sentiment service"""
        sentiment = get_sentiment_by_symbol("AAPL")
        assert sentiment["symbol"] == "AAPL"
        assert "sentiment_score" in sentiment
        assert 0 <= sentiment["sentiment_score"] <= 1

    def test_get_historical_prices(self):
        """Test historical prices service"""
        prices = get_historical_prices("AAPL", days=30)
        assert prices["symbol"] == "AAPL"
        assert len(prices["prices"]) == 30
        assert len(prices["dates"]) == 30

    def test_get_market_overview(self):
        """Test market overview service"""
        overview = get_market_overview()
        assert "total_symbols" in overview
        assert "active_signals" in overview
        assert overview["active_signals"] <= overview["total_symbols"]
