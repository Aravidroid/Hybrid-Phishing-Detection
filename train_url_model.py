import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

from feature_extractor import extract_url_features

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("phishing_urls.csv")

# -----------------------------
# 2. Extract features
# -----------------------------
feature_list = []

print("⚙️ Extracting URL features...")

for url in df["url"]:
    features = extract_url_features(url)
    feature_list.append(features)

X = pd.DataFrame(feature_list)
y = df["label"]

# -----------------------------
# 3. Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# 4. Train model
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# -----------------------------
# 5. Evaluate
# -----------------------------
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# 6. Save model
# -----------------------------
joblib.dump(model, "url_phishing_model.pkl")
joblib.dump(X.columns.tolist(), "url_feature_names.pkl")

print("\nURL model saved successfully!")