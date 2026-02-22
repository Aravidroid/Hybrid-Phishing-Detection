# 🛡️Hybrid Phishing Detection Engine

A hybrid phishing detection system that combines:

-   🧠 NLP-based social engineering detection
-   🌐 URL structural & lexical analysis
-   ⚖ Rule-based high precision engine
-   🔀 Decision fusion logic

Built entirely in Python.

------------------------------------------------------------------------

## 🚀 Project Overview

Metaverse Guard is a multi-layer phishing detection engine designed to
simulate real-world security systems.

Instead of relying on a single model, it combines:

Incoming Message\
↓\
Text → NLP Model (TF-IDF + Naive Bayes)
↓\
URL → Feature Extractor → RandomForest Model
↓\
Rule Engine (High-confidence checks)
↓\
Decision Fusion Layer
↓\
Final Security Decision

This layered approach reduces false positives and improves robustness.

------------------------------------------------------------------------

## 🧠 Detection Layers

### 1️⃣ NLP Model (Social Engineering Detection)

-   TF-IDF vectorization\
-   N-gram range (1,2)\
-   Multinomial Naive Bayes\
-   Detects urgency, financial manipulation, phishing language

Example: "URGENT: TRANSFER FUNDS NOW"

------------------------------------------------------------------------

### 2️⃣ URL Machine Learning Model

-   RandomForestClassifier
-   Custom feature extraction
-   Balanced class weighting

Extracted features include:

-   URL length
-   Domain length
-   Path length
-   Dot count
-   Subdomain count
-   Suspicious keywords
-   Digit ratio
-   Domain entropy
-   Suspicious TLD detection
-   IP-based domain detection

------------------------------------------------------------------------

### 3️⃣ Rule-Based Engine

High-confidence rules:

-   IP-based domains
-   Excessive subdomains
-   Suspicious keyword concentration
-   Obvious structural anomalies

------------------------------------------------------------------------

### 4️⃣ Decision Fusion

Combines:

-   NLP risk score
-   URL ML score
-   Rule engine signals

Outputs:

-   ✅ CLEAN
-   ⚠ WARNING
-   🚫 URL BLOCKED
-   🚨 CRITICAL BLOCK

------------------------------------------------------------------------

## ⚙ Installation

pip install pandas scikit-learn joblib

------------------------------------------------------------------------

## 🧪 Training Models

Train NLP model: python train_nlp.py

Train URL model: python train_url_model.py

------------------------------------------------------------------------

## ▶ Run Detection Engine

python metaverse_guard.py

------------------------------------------------------------------------

## 🔬 Key Engineering Challenges Solved

-   Dataset distribution bias\
-   Structural overfitting\
-   Subdomain miscalculation\
-   www normalization inconsistencies\
-   Feature alignment between training & inference\
-   False positive tuning

------------------------------------------------------------------------

## 🛠 Technologies Used

-   Python 3.12
-   Scikit-learn
-   Pandas
-   RandomForestClassifier
-   Multinomial Naive Bayes
-   TF-IDF
-   Custom feature engineering

------------------------------------------------------------------------

## 🎯 Future Improvements

-   Domain reputation integration
-   WHOIS age lookup
-   XGBoost upgrade
-   FastAPI deployment
-   Real-time dashboard
-   Cloud deployment

------------------------------------------------------------------------

## 👨‍💻 Author

Aravind A\
Cybersecurity & Machine Learning Enthusiast

------------------------------------------------------------------------

This project demonstrates hybrid security architecture thinking, feature
engineering, model debugging, and real-world phishing detection
challenges.
