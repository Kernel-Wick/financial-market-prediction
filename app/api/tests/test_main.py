"""Tests for FastAPI endpoints"""

from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from main import app

client = TestClient(app)


class TestHealthAndBasic:
    def test_health(self):
        """Test API health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "market-api"

    def test_market_overview(self):
        """Test market overview endpoint"""
        response = client.get("/api/v1/market/overview")
        assert response.status_code == 200
        data = response.json()
        assert "total_symbols" in data
        assert "active_signals" in data
        assert "market_status" in data

    def test_market_signals(self):
        """Test market signals endpoint"""
        response = client.get("/api/v1/market/signals")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        # Validate structure
        signal = data[0]
        assert "symbol" in signal
        assert "signal" in signal
        assert "confidence" in signal
        assert signal["signal"] in ["buy", "sell", "hold"]
        assert 0 <= signal["confidence"] <= 1

    def test_sentiment_by_symbol(self):
        """Test sentiment endpoint"""
        response = client.get("/api/v1/market/sentiment/AAPL")
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "AAPL"
        assert "sentiment_score" in data
        assert "sentiment_label" in data
        assert 0 <= data["sentiment_score"] <= 1

    def test_historical_data(self):
        """Test historical data endpoint"""
        response = client.get("/api/v1/market/historical/AAPL?days=30")
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "AAPL"
        assert "prices" in data
        assert "dates" in data
        assert len(data["prices"]) == 30
        assert len(data["dates"]) == 30
