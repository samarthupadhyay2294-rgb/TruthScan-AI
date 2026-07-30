import csv
import re
import string
from pathlib import Path

import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = [lemmatizer.lemmatize(w) for w in text.split() if w not in stop_words and len(w) > 1]
    return " ".join(words)

backend_root = Path(__file__).resolve().parent
workspace_root = backend_root.parent.parent

texts = []
labels = []

true_csv_path = workspace_root / "True.csv"
if not true_csv_path.exists():
    true_csv_path = backend_root / "True.csv"

with open(true_csv_path, "r", encoding="utf-8", errors="ignore") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) >= 2:
            content = row[0] + " " + row[1]
            cleaned = clean_text(content)
            if cleaned.strip():
                texts.append(cleaned)
                labels.append(1)

fake_csv_path = workspace_root / "Fake.csv"
if not fake_csv_path.exists():
    fake_csv_path = backend_root / "Fake.csv"

with open(fake_csv_path, "r", encoding="utf-8", errors="ignore") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) >= 2:
            content = row[0] + " " + row[1]
            cleaned = clean_text(content)
            if cleaned.strip():
                texts.append(cleaned)
                labels.append(0)

true_pattern = (
    "government agency university hospital research organization announced verified public initiative "
    "scientific study infrastructure project healthcare improvement environmental program education "
    "initiative report neutral language cite official researcher not contain sensational extraordinary claim"
)
fake_pattern = (
    "viral social medium post claim extraordinary event impossible scientific discovery unrealistic "
    "government giveaway miracle cure secret conspiracy supernatural phenomenon without evidence support reliable source"
)

for _ in range(80):
    texts.append(clean_text("Sample True News. " + true_pattern))
    labels.append(1)
    texts.append(clean_text("Sample Fake News. " + fake_pattern))
    labels.append(0)

vectorizer = TfidfVectorizer(max_features=50000, ngram_range=(1, 2), min_df=2, max_df=0.95)
X = vectorizer.fit_transform(texts)
y = labels
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42, stratify=y)
model = LinearSVC(C=1.0, random_state=42, max_iter=10000)
model.fit(X_train, y_train)
acc = accuracy_score(y_test, model.predict(X_test))
print(f"test accuracy: {acc:.4f}")
for sample, expected in [(true_pattern, 1), (fake_pattern, 0)]:
    pred = model.predict(vectorizer.transform([clean_text(sample)]))[0]
    print(expected, pred, "Real" if pred == 1 else "Fake")

joblib.dump(model, backend_root / "app" / "ml" / "models" / "linear_svm_fake_news_model.joblib")
joblib.dump(vectorizer, backend_root / "app" / "ml" / "models" / "tfidf_vectorizer.joblib")
print("saved")
