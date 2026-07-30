from typing import Any

import numpy as np
from sklearn.svm import LinearSVC

SUSPICIOUS_WORDS = {
    "shocking",
    "unbelievable",
    "secret",
    "conspiracy",
    "hoax",
    "breaking",
    "exclusive",
    "miracle",
    "cure",
    "anonymous",
    "sources",
    "rumor",
    "viral",
    "clickbait",
    "exposed",
    "bombshell",
    "outrage",
    "scandal",
    "coverup",
}


def extract_explainability(
    model: LinearSVC,
    vectorizer: Any,
    cleaned_text: str,
    predicted_label: int,
    top_n: int = 10,
) -> dict[str, Any]:
    feature_names = vectorizer.get_feature_names_out()
    coefficients = model.coef_[0]

    text_features = vectorizer.transform([cleaned_text])
    nonzero_indices = text_features.nonzero()[1]

    contributions: list[dict[str, Any]] = []
    for idx in nonzero_indices:
        coef = float(coefficients[idx])
        tfidf_value = float(text_features[0, idx])
        contribution = coef * tfidf_value
        direction = "supports_real" if contribution > 0 else "supports_fake"
        contributions.append(
            {
                "keyword": feature_names[idx],
                "contribution": round(contribution, 6),
                "coefficient": round(coef, 6),
                "tfidf": round(tfidf_value, 6),
                "direction": direction,
            }
        )

    if predicted_label == 1:
        contributions.sort(key=lambda x: x["contribution"], reverse=True)
    else:
        contributions.sort(key=lambda x: x["contribution"])

    top_keywords = contributions[:top_n]

    words_in_text = set(cleaned_text.split())
    suspicious_found = sorted(words_in_text.intersection(SUSPICIOUS_WORDS))

    global_top_indices = np.argsort(np.abs(coefficients))[-top_n:][::-1]
    global_keywords = [
        {
            "keyword": feature_names[i],
            "coefficient": round(float(coefficients[i]), 6),
        }
        for i in global_top_indices
    ]

    return {
        "top_keywords": top_keywords,
        "suspicious_words": suspicious_found,
        "global_important_features": global_keywords,
    }
