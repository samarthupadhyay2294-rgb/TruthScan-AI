import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

_nltk_initialized = False


def _ensure_nltk_data() -> None:
    global _nltk_initialized
    if _nltk_initialized:
        return
    for resource in ("stopwords", "wordnet", "omw-1.4"):
        try:
            nltk.data.find(
                f"corpora/{resource}" if resource == "stopwords" else f"corpora/{resource}"
            )
        except LookupError:
            nltk.download(resource, quiet=True)
    _nltk_initialized = True


_ensure_nltk_data()

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text: str) -> str:
    text = text.lower()

    text = re.sub(r"http\S+|www\S+", "", text)

    text = re.sub(r"<.*?>", "", text)

    text = re.sub(r"\d+", "", text)

    text = text.translate(str.maketrans("", "", string.punctuation))

    words = [
        lemmatizer.lemmatize(word)
        for word in text.split()
        if word not in stop_words
    ]

    return " ".join(words)
