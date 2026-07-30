from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class HistoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    label: int
    label_name: str
    confidence: float
    source: str
    filename: Optional[str] = None
    created_at: datetime


class HistoryListResponse(BaseModel):
    items: list[HistoryItemResponse]
    total: int
    page: int
    page_size: int
