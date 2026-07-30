from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prediction_id: int
    title: str
    summary: Optional[str] = None
    content: dict[str, Any]
    pdf_path: Optional[str] = None
    created_at: datetime


class ReportListResponse(BaseModel):
    items: list[ReportResponse]
    total: int
