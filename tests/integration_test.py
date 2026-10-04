"""Integration tests for full stack"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/api")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/ml")))

from fastapi.testclient import TestClient
from main import app
from services import get_market_signals
from sentiment import analyze_sentiment
from forecasting import forecast

client = TestClient(app)


class TestFullIntegration:
    def test_api_to_service_flow(self):
        """Test that API correctly uses service layer"""
        # API call
        response = client.get("/api/v1/market/signals")
        api_signals = response.json()
        
        # Service call
        service_signals = get_market_signals()
        
        # Verify alignment
        assert len(api_signals) == len(service_signals)
        assert api_signals[0]["symbol"] == service_signals[0]["symbol"]

    def test_sentiment_pipeline(self):
        """Test sentiment analysis pipeline"""
        text = "The market is showing strong bullish signals today"
        result = analyze_sentiment(text)
        assert "sentiment" in result
        assert "score" in result
        assert result["sentiment"] in ["positive", "negative", "neutral"]
        assert 0 <= result["score"] <= 1

    def test_forecasting_pipeline(self):
        """Test forecasting pipeline"""
        prices = [100, 101, 102, 103, 105]
        result = forecast("AAPL", historical_prices=prices)
        assert "forecasted_prices" in result
        assert len(result["forecasted_prices"]) == 5

    def test_end_to_end_signal_flow(self):
        """Test complete flow: API -> Service -> Model"""
        # 1. Get signals from API
        response = client.get("/api/v1/market/signals")
        signals = response.json()
        assert len(signals) > 0
        
        # 2. Test sentiment for each signal
        for signal in signals:
            sentiment_response = client.get(f"/api/v1/market/sentiment/{signal['symbol']}")
            assert sentiment_response.status_code == 200
            
            sentiment_data = sentiment_response.json()
            assert sentiment_data["sentiment_score"] >= 0
        
        # 3. Test historical data
        historical_response = client.get("/api/v1/market/historical/AAPL?days=30")
        assert historical_response.status_code == 200
        historical_data = historical_response.json()
        assert len(historical_data["prices"]) == 30
