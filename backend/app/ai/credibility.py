from typing import Any

from app.ai.sentiment import analyze_sentiment
from app.ml.explainability import SUSPICIOUS_WORDS


def calculate_credibility_score(
    text: str,
    ml_confidence: float,
    predicted_label: int,
    suspicious_words: list[str],
) -> dict[str, Any]:
    words = set(text.lower().split())
    suspicious_ratio = len(words.intersection(SUSPICIOUS_WORDS)) / max(len(words), 1)
    sentiment = analyze_sentiment(text)

    base = ml_confidence if predicted_label == 1 else (1.0 - ml_confidence)
    penalty = min(suspicious_ratio * 0.5, 0.3)
    sentiment_adjustment = -0.05 if sentiment["label"] == "negative" else 0.02

    score = max(0.0, min(1.0, base - penalty + sentiment_adjustment))

    if score >= 0.75:
        rating = "high"
    elif score >= 0.5:
        rating = "medium"
    else:
        rating = "low"

    return {
        "score": round(score, 4),
        "rating": rating,
        "factors": {
            "ml_confidence": ml_confidence,
            "suspicious_word_ratio": round(suspicious_ratio, 4),
            "sentiment": sentiment["label"],
        },
    }
