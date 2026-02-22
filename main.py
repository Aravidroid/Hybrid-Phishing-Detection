import joblib
import pandas as pd
from feature_extractor import extract_url_features

# -----------------------------
# Load models
# -----------------------------
print("⚙️ Loading Models...")

nlp_brain = joblib.load("nlp_phishing_model.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")

url_brain = joblib.load("url_phishing_model.pkl")
url_feature_names = joblib.load("url_feature_names.pkl")

print("✅ System Ready.\n")

# -----------------------------
# Rule Engine (High-Precision)
# -----------------------------
def rule_based_url_risk(features: dict) -> bool:
    
    # Block IP-based domains
    if features["IsDomainIP"] == 1:
        return True

    # Too many subdomains
    if features["NoOfSubDomain"] >= 3:
        return True

    # Suspicious keywords
    if features["SuspiciousKeywords"] >= 2:
        return True

    # Extremely high entropy domain
    if features["DomainEntropy"] > 4.0:
        return True

    return False


# -----------------------------
# Simulation Stream
# -----------------------------
messages = [
    ("Friend1", "Join our discord", "https://discord.com/gaming"),
    ("Hacker1", "Check this funny picture", "http://secure-login.apple-id-verify.xyz/auth"),
    ("Scammer", "URGENT: TRANSFER FUNDS NOW OR ACCOUNT LOCK", "https://www.abcaccount.com"),
    ("BotNet", "FREE CRYPTO GIVEAWAY CLAIM FAST", "http://192.168.1.55/wallet-drainer.exe")
]

print(f"{'USER':<10} | {'NLP RISK':<10} | {'URL ML':<10} | {'RULE':<6} | {'FINAL SCORE':<12} | {'DECISION'}")
print("-" * 110)

for user, text, url in messages:

    # -----------------------------
    # 1. NLP Risk (Social Engineering)
    # -----------------------------
    text_vec = tfidf.transform([text])
    nlp_score = nlp_brain.predict_proba(text_vec)[0][1]

    # -----------------------------
    # 2. URL Feature Extraction
    # -----------------------------
    url_features = extract_url_features(url)
    url_df = pd.DataFrame([url_features])

    # Align features with training columns
    url_df = url_df.reindex(columns=url_feature_names, fill_value=0)

    url_ml_score = url_brain.predict_proba(url_df)[0][1]

    # -----------------------------
    # 3. Rule-Based URL Risk
    # -----------------------------
    rule_risk = rule_based_url_risk(url_features)

    # -----------------------------
    # 4. Decision Fusion (Weighted)
    # -----------------------------
    final_score = (
        0.4 * nlp_score +
        0.4 * url_ml_score +
        0.2 * int(rule_risk)
    )

    decision = "✅ CLEAN"

    if final_score >= 0.75:
        decision = "🚨 CRITICAL BLOCK"
    elif final_score >= 0.55:
        decision = "🚫 URL BLOCKED"
    elif final_score >= 0.40:
        decision = "⚠️ WARNING"

    # -----------------------------
    # Display
    # -----------------------------
    print(
        f"{user:<10} | "
        f"{nlp_score*100:>6.2f}%   | "
        f"{url_ml_score*100:>6.2f}%   | "
        f"{str(rule_risk):<6} | "
        f"{final_score*100:>8.2f}%   | "
        f"{decision}"
    )

print("\n✅ Simulation Complete.")
