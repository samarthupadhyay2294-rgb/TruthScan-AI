from typing import Any


POSITIVE_WORDS = {
    "good",
    "great",
    "excellent",
    "positive",
    "success",
    "happy",
    "hope",
    "trust",
    "verified",
    "confirmed",
}

NEGATIVE_WORDS = {
    "bad",
    "terrible",
    "fake",
    "false",
    "hoax",
    "scandal",
    "fear",
    "danger",
    "crisis",
    "lie",
    "misleading",
}


def analyze_sentiment(text: str) -> dict[str, Any]:
    words = text.lower().split()
    positive = sum(1 for w in words if w in POSITIVE_WORDS)
    negative = sum(1 for w in words if w in NEGATIVE_WORDS)
    total = positive + negative

    if total == 0:
        compound = 0.0
        label = "neutral"
    else:
        compound = (positive - negative) / total
        if compound > 0.15:
            label = "positive"
        elif compound < -0.15:
            label = "negative"
        else:
            label = "neutral"

    return {
        "label": label,
        "compound": round(compound, 4),
        "positive_count": positive,
        "negative_count": negative,
    }
