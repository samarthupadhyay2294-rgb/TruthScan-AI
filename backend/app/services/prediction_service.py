from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.bias_detector import detect_bias
from app.ai.credibility import calculate_credibility_score
from app.ai.keyword_extractor import extract_keywords, extract_named_entities
from app.ai.sentiment import analyze_sentiment
from app.ai.summarizer import summarize_text
from app.database import crud
from app.database.models import Prediction, User
from app.ml.predictor import predictor
from app.ml.utils import build_analysis_payload
from app.schemas.prediction import (
    AIAnalysisResult,
    ExplainabilityResult,
    PredictResultResponse,
    PredictionResponse,
)


class PredictionService:
    async def run_ai_analysis(
        self, text: str, ml_result: dict[str, Any]
    ) -> dict[str, Any]:
        explainability = ml_result.get("explainability", {})
        suspicious = explainability.get("suspicious_words", [])

        credibility = calculate_credibility_score(
            text=text,
            ml_confidence=ml_result["confidence"],
            predicted_label=ml_result["label"],
            suspicious_words=suspicious,
        )

        return {
            "summary": summarize_text(text),
            "keywords": extract_keywords(text) + extract_named_entities(text),
            "sentiment": analyze_sentiment(text),
            "credibility_score": credibility["score"] if isinstance(credibility, dict) else credibility,
            "bias": detect_bias(text),
        }

    async def predict_text(
        self,
        db: AsyncSession,
        *,
        user: Optional[User] = None,
        text: str,
        source: str = "manual",
        filename: Optional[str] = None,
    ) -> PredictResultResponse:
        ml_result = predictor.predict(text)
        ai_analysis = await self.run_ai_analysis(text, ml_result)
        analysis = build_analysis_payload(ml_result, ai_analysis)

        prediction = await crud.create_prediction(
            db,
            user_id=user.id if user else None,
            text=text,
            cleaned_text=ml_result["cleaned_text"],
            label=ml_result["label"],
            label_name=ml_result["label_name"],
            confidence=ml_result["confidence"],
            source=source,
            filename=filename,
            analysis=analysis,
        )

        return PredictResultResponse(
            prediction=PredictionResponse.model_validate(prediction),
            explainability=ExplainabilityResult(**ml_result["explainability"]),
            ai_analysis=AIAnalysisResult(**ai_analysis),
        )

    async def get_prediction(
        self, db: AsyncSession, prediction_id: int, user_id: int
    ) -> Optional[Prediction]:
        return await crud.get_prediction_by_id(db, prediction_id, user_id)


prediction_service = PredictionService()
