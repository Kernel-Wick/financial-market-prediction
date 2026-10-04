"""Tests for forecasting module"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from forecasting import forecast, forecast_with_volatility


class TestForecasting:
    def test_forecast(self):
        """Test basic forecasting"""
        result = forecast("AAPL")
        assert result["symbol"] == "AAPL"
        assert "forecasted_prices" in result
        assert "confidence_scores" in result
        assert len(result["forecasted_prices"]) == 5
        assert len(result["confidence_scores"]) == 5
        # All prices should be positive
        assert all(p > 0 for p in result["forecasted_prices"])
        # All confidence scores between 0 and 1
        assert all(0 <= c <= 1 for c in result["confidence_scores"])

    def test_forecast_with_historical(self):
        """Test forecasting with historical data"""
        historical = [100, 102, 104, 103, 105]
        result = forecast("MSFT", historical_prices=historical)
        assert result["symbol"] == "MSFT"
        assert len(result["forecasted_prices"]) == 5
        # Forecast should follow trend (upward in this case)
        assert result["forecasted_prices"][-1] > 100

    def test_forecast_with_volatility(self):
        """Test forecast with volatility analysis"""
        historical = [100, 95, 105, 98, 110, 102]
        result = forecast_with_volatility("NVDA", historical_prices=historical)
        assert "volatility" in result
        assert 0 <= result["volatility"] <= 1
        # High volatility should reduce confidence
        base_result = forecast("NVDA", historical_prices=historical)
        # Due to volatility, confidence should generally be lower or equal
        assert all(
            result["confidence_scores"][i] <= base_result["confidence_scores"][i]
            for i in range(5)
        )
