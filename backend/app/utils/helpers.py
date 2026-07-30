import math
from datetime import datetime, timezone
from typing import Any, Generic, Sequence, TypeVar

T = TypeVar("T")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def paginate(
    items: Sequence[T],
    *,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": list(items[start:end]),
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, math.ceil(total / page_size)) if page_size else 1,
    }


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def normalize_label_name(label: int) -> str:
    return "Fake" if label == 0 else "Real"


def to_frontend_label(label: int, confidence: float, uncertain_threshold: float = 0.55) -> str:
    if abs(confidence - 0.5) < (0.5 - uncertain_threshold):
        return "UNCERTAIN"
    return "REAL" if label == 1 else "FAKE"


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class PaginatedResult(Generic[T]):
    def __init__(
        self,
        items: list[T],
        total: int,
        page: int,
        page_size: int,
    ) -> None:
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = max(1, math.ceil(total / page_size)) if page_size else 1
