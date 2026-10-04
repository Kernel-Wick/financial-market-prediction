"""Time-series forecasting module"""

from typing import Dict, List
import statistics


def forecast(symbol: str, historical_prices: List[float] = None) -> Dict:
    """
    Generate price forecast for a symbol.
    Uses simple exponential smoothing as baseline.
    
    Args:
        symbol: Stock symbol
        historical_prices: List of historical prices for trend analysis
    
    Returns:
        Dict with forecasted_prices and confidence_scores
    """
    if historical_prices is None:
        historical_prices = [100.0, 101.5, 103.0, 102.5, 104.0]
    
    # Simple exponential smoothing
    if len(historical_prices) < 2:
        last_price = historical_prices[0] if historical_prices else 100.0
        trend = 1.01
    else:
        last_price = historical_prices[-1]
        # Calculate simple trend
        trend = historical_prices[-1] / historical_prices[0] if historical_prices[0] > 0 else 1.01
    
    # Generate 5-day forecast
    forecasted_prices = []
    confidence_scores = []
    current = last_price
    
    for i in range(5):
        current = current * (1.0 + (trend - 1.0) * 0.1)  # Dampen trend
        forecasted_prices.append(round(current, 2))
        # Confidence decreases with forecast horizon
        confidence = max(0.5, 0.85 - i * 0.08)
        confidence_scores.append(round(confidence, 2))
    
    return {
        "symbol": symbol,
        "forecasted_prices": forecasted_prices,
        "confidence_scores": confidence_scores,
        "model_version": "baseline_v0.1",
    }


def forecast_with_volatility(symbol: str, historical_prices: List[float]) -> Dict:
    """
    Generate forecast with volatility-based confidence intervals.
    """
    base_forecast = forecast(symbol, historical_prices)
    
    # Calculate volatility
    if len(historical_prices) > 1:
        mean_price = statistics.mean(historical_prices)
        variance = sum((p - mean_price) ** 2 for p in historical_prices) / len(historical_prices)
        volatility = (variance ** 0.5) / mean_price if mean_price > 0 else 0.1
    else:
        volatility = 0.1
    
    # Adjust confidence based on volatility
    adjusted_confidence = [max(0.3, score - volatility * 0.5) for score in base_forecast["confidence_scores"]]
    
    return {
        **base_forecast,
        "confidence_scores": adjusted_confidence,
        "volatility": round(volatility, 3),
    }
