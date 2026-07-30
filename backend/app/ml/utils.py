from typing import Any


def label_to_name(label: int) -> str:
    return "Fake" if label == 0 else "Real"


def truncate_text(text: str, max_length: int = 200) -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def build_analysis_payload(
    ml_result: dict[str, Any],
    ai_analysis: dict[str, Any],
) -> dict[str, Any]:
    return {
        "ml": {
            "label": ml_result["label"],
            "label_name": ml_result["label_name"],
            "confidence": ml_result["confidence"],
            "decision_score": ml_result.get("decision_score"),
            "explainability": ml_result.get("explainability", {}),
        },
        "ai": ai_analysis,
    }
