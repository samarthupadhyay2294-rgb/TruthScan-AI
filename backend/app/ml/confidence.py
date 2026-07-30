import math


def decision_function_to_confidence(decision_score: float) -> float:
    """Convert LinearSVC decision function output to a 0-1 confidence score."""
    confidence = 1.0 / (1.0 + math.exp(-decision_score))
    return round(min(max(confidence, 0.0), 1.0), 4)
