"""Tests for sentiment analysis"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from sentiment import analyze_sentiment, batch_analyze_sentiment


class TestSentimentAnalysis:
    def test_analyze_sentiment_positive(self):
        """Test positive sentiment detection"""
        result = analyze_sentiment("This is a great product! Excellent performance!")
        assert "sentiment" in result
        assert "score" in result
        assert result["sentiment"] == "positive"
        assert result["score"] > 0.5

    def test_analyze_sentiment_negative(self):
        """Test negative sentiment detection"""
        result = analyze_sentiment("This is terrible and awful!")
        assert result["sentiment"] == "negative"
        assert result["score"] < 0.5

    def test_analyze_sentiment_neutral(self):
        """Test neutral sentiment detection"""
        result = analyze_sentiment("The market opened today with mixed signals.")
        assert result["sentiment"] == "neutral"
        assert 0.45 < result["score"] < 0.55

    def test_batch_analyze_sentiment(self):
        """Test batch sentiment analysis"""
        texts = [
            "Great results!",
            "Terrible performance",
            "Average day",
        ]
        results = batch_analyze_sentiment(texts)
        assert len(results) == 3
        assert all("sentiment" in r and "score" in r for r in results)
