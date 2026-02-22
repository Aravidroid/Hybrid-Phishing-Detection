import pandas as pd
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score


# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("phishing_nlp.csv")  # update filename

# -----------------------------
# 2. Combine subject + body
# -----------------------------
df["text"] = (
    df["subject"].fillna("") + " " + df["body"].fillna("")
)

# -----------------------------
# 3. Basic text cleaning
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", " URL ", text)   # replace URLs
    text = re.sub(r"\d+", " ", text)            # remove numbers
    text = re.sub(r"[^\w\s]", " ", text)        # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()    # remove extra spaces
    return text

df["text"] = df["text"].apply(clean_text)

X = df["text"]
y = df["label"]

# -----------------------------
# 4. Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# 5. TF-IDF (BEST PARAMETERS)
# -----------------------------
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),      # uni + bi-grams (VERY IMPORTANT)
    max_df=0.9,              # ignore very common words
    min_df=3,                # ignore rare noise
    max_features=15000,      # good balance of speed & accuracy
    sublinear_tf=True        # better weighting
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------------
# 6. Train Naive Bayes model
# -----------------------------
model = MultinomialNB(alpha=0.1)  # smoothing (best for phishing)

model.fit(X_train_vec, y_train)

# -----------------------------
# 7. Evaluate
# -----------------------------
y_pred = model.predict(X_test_vec)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# 8. Save model & vectorizer
# -----------------------------
joblib.dump(model, "nlp_phishing_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("\nModel and vectorizer saved successfully!")