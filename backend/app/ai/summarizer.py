import re
from typing import Optional


def summarize_text(text: str, max_sentences: int = 3) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return text[:300]
    if len(sentences) <= max_sentences:
        return " ".join(sentences)
    ranked = sorted(
        enumerate(sentences),
        key=lambda item: len(item[1].split()),
        reverse=True,
    )
    top_indices = sorted(idx for idx, _ in ranked[:max_sentences])
    return " ".join(sentences[i] for i in top_indices)
