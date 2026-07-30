from typing import Any

POLITICAL_KEYWORDS = {
    "democrat",
    "republican",
    "liberal",
    "conservative",
    "left",
    "right",
    "government",
    "president",
    "election",
}

EMOTIONAL_KEYWORDS = {
    "outrage",
    "shocking",
    "unbelievable",
    "amazing",
    "terrible",
    "horrific",
    "miracle",
}


def detect_bias(text: str) -> dict[str, Any]:
    words = text.lower().split()
    word_set = set(words)

    political_hits = word_set.intersection(POLITICAL_KEYWORDS)
    emotional_hits = word_set.intersection(EMOTIONAL_KEYWORDS)

    political_score = min(len(political_hits) / 5.0, 1.0)
    emotional_score = min(len(emotional_hits) / 5.0, 1.0)
    overall = round((political_score * 0.6 + emotional_score * 0.4), 4)

    if overall >= 0.6:
        level = "high"
    elif overall >= 0.3:
        level = "moderate"
    else:
        level = "low"

    return {
        "bias_score": overall,
        "bias_level": level,
        "political_keywords": sorted(political_hits),
        "emotional_keywords": sorted(emotional_hits),
    }
