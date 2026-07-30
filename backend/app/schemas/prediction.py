from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class PredictRequest(BaseModel):
    text: str = Field(min_length=10, max_length=50000)


class ExplainabilityResult(BaseModel):
    top_keywords: list[dict[str, Any]] = Field(default_factory=list)
    suspicious_words: list[str] = Field(default_factory=list)


class AIAnalysisResult(BaseModel):
    summary: Optional[str] = None
    keywords: list[str] = Field(default_factory=list)
    sentiment: Optional[dict[str, Any]] = None
    credibility_score: Optional[float] = None
    bias: Optional[dict[str, Any]] = None


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    label: int
    label_name: str
    confidence: float
    source: str
    filename: Optional[str] = None
    analysis: Optional[dict[str, Any]] = None
    created_at: datetime


class PredictResultResponse(BaseModel):
    prediction: PredictionResponse
    explainability: ExplainabilityResult
    ai_analysis: AIAnalysisResult
