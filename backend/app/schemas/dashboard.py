from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class DashboardStatsResponse(BaseModel):
    total_predictions: int
    fake_count: int
    real_count: int
    avg_confidence: float
    fake_percentage: float
    real_percentage: float


class RecentPredictionItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    label: int
    label_name: str
    confidence: float
    created_at: datetime


class DashboardResponse(BaseModel):
    stats: DashboardStatsResponse
    recent_predictions: list[RecentPredictionItem]
    trend: list[dict[str, Any]] = []
