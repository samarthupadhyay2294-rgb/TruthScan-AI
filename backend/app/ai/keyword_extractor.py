import re
from collections import Counter
from typing import List

from app.ml.preprocessing import clean_text

STOP_KEYWORDS = {
    "said",
    "say",
    "says",
    "would",
    "could",
    "also",
    "one",
    "two",
    "new",
    "year",
    "time",
    "people",
    "report",
    "news",
}


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    cleaned = clean_text(text)
    words = [w for w in cleaned.split() if len(w) > 3 and w not in STOP_KEYWORDS]
    if not words:
        return []
    counts = Counter(words)
    return [word for word, _ in counts.most_common(top_n)]


def extract_named_entities(text: str) -> List[str]:
    candidates = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)
    return list(dict.fromkeys(candidates))[:10]
