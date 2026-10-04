"""Sentiment analysis module"""

from typing import Dict


def analyze_sentiment(text: str) -> Dict:
    """
    Analyze sentiment of a given text.
    Returns dict with 'sentiment' label and 'score' (0-1).
    
    Placeholder for now - can be replaced with transformers/BERT later.
    """
    text_lower = text.lower()
    
    # Simple keyword-based sentiment (mock)
    positive_words = ["great", "excellent", "bullish", "strong", "good", "amazing"]
    negative_words = ["terrible", "bad", "bearish", "weak", "poor", "awful"]
    
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        sentiment = "positive"
        score = min(0.95, 0.5 + pos_count * 0.15)
    elif neg_count > pos_count:
        sentiment = "negative"
        score = max(0.05, 0.5 - neg_count * 0.15)
    else:
        sentiment = "neutral"
        score = 0.5
    
    return {"sentiment": sentiment, "score": score}


def batch_analyze_sentiment(texts: list) -> list:
    """Analyze sentiment for multiple texts"""
    return [analyze_sentiment(text) for text in texts]
