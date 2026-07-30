from pathlib import Path
from typing import Any, Optional

import joblib
from sklearn.svm import LinearSVC

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.logging import get_logger
from app.ml.confidence import decision_function_to_confidence
from app.ml.explainability import extract_explainability
from app.ml.preprocessing import clean_text

logger = get_logger(__name__)

LABEL_MAP = {0: "Fake", 1: "Real"}


class ModelPredictor:
    def __init__(self) -> None:
        self.model: Optional[LinearSVC] = None
        self.vectorizer: Optional[Any] = None
        self._loaded = False

    def _resolve_artifact_path(self, relative_path: str) -> Path:
        candidate = Path(relative_path)
        if candidate.is_absolute():
            return candidate

        backend_root = Path(__file__).resolve().parents[2]
        resolved = backend_root / candidate
        if resolved.exists():
            return resolved

        return candidate

    def load(self) -> None:
        model_path = self._resolve_artifact_path(settings.ML_MODEL_PATH)
        vectorizer_path = self._resolve_artifact_path(settings.ML_VECTORIZER_PATH)

        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not vectorizer_path.exists():
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")

        logger.info("Loading ML model from %s", model_path)
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self._loaded = True
        logger.info("ML model and vectorizer loaded successfully")

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def predict(self, text: str) -> dict[str, Any]:
        if not self._loaded or self.model is None or self.vectorizer is None:
            raise AppException("ML model is not loaded", status_code=503)

        cleaned = clean_text(text)
        if not cleaned.strip():
            raise AppException("Text is empty after preprocessing")

        features = self.vectorizer.transform([cleaned])
        label = int(self.model.predict(features)[0])
        decision_score = float(self.model.decision_function(features)[0])
        confidence = decision_function_to_confidence(decision_score)
        explainability = extract_explainability(
            self.model, self.vectorizer, cleaned, label
        )

        return {
            "cleaned_text": cleaned,
            "label": label,
            "label_name": LABEL_MAP.get(label, "Unknown"),
            "confidence": confidence,
            "decision_score": decision_score,
            "explainability": explainability,
        }


predictor = ModelPredictor()
