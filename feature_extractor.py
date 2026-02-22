import re
import math
from urllib.parse import urlparse
import ipaddress

# ---------------------------------
# Helper: Check if domain is IP
# ---------------------------------
def is_ip(domain):
    try:
        ipaddress.ip_address(domain)
        return 1
    except:
        return 0

# ---------------------------------
# Helper: Shannon Entropy
# ---------------------------------
def shannon_entropy(data):
    if not data:
        return 0
    prob = [float(data.count(c)) / len(data) for c in dict.fromkeys(list(data))]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy

# ---------------------------------
# Main Feature Extraction Function
# ---------------------------------
def extract_url_features(url):

    try:
        parsed = urlparse(str(url))
        domain = parsed.netloc.lower()
        path = parsed.path.lower()

        # 🔥 Normalize www BEFORE ANY FEATURE
        if domain.startswith("www."):
            domain = domain[4:]

        # 🔥 Reconstruct normalized URL
        normalized_url = f"{parsed.scheme}://{domain}{path}"

    except:
        return {
            "URLLength": 0,
            "DomainLength": 0,
            "PathLength": 0,
            "IsDomainIP": 0,
            "NoOfDots": 0,
            "NoOfSubDomain": 0,
            "HasHyphen": 0,
            "HasAtSymbol": 0,
            "HasDoubleSlash": 0,
            "SuspiciousKeywords": 0,
            "DomainEntropy": 0,
            "DigitCount": 0,
            "DigitRatio": 0,
            "SuspiciousTLD": 0
        }

    features = {}

    # -------------------------
    # Use NORMALIZED URL for structural features
    # -------------------------
    features["URLLength"] = len(normalized_url)
    features["DomainLength"] = len(domain)
    features["PathLength"] = len(path)
    features["IsDomainIP"] = is_ip(domain)

    features["NoOfDots"] = normalized_url.count(".")

    parts = domain.split(".")
    features["NoOfSubDomain"] = max(len(parts) - 2, 0)

    features["HasHyphen"] = 1 if "-" in domain else 0
    features["HasAtSymbol"] = 1 if "@" in normalized_url else 0
    features["HasDoubleSlash"] = 1 if normalized_url.count("//") > 1 else 0

    # -------------------------
    # Keywords
    # -------------------------
    suspicious_keywords = [
        "login", "verify", "secure", "account",
        "update", "bank", "free", "bonus", "crypto",
        "signin", "confirm", "wallet", "payment"
    ]

    features["SuspiciousKeywords"] = sum(
        1 for word in suspicious_keywords if word in normalized_url.lower()
    )

    # -------------------------
    # Entropy
    # -------------------------
    features["DomainEntropy"] = shannon_entropy(domain)

    # -------------------------
    # Digit features
    # -------------------------
    digit_count = sum(c.isdigit() for c in domain)
    features["DigitCount"] = digit_count
    features["DigitRatio"] = digit_count / len(domain) if len(domain) > 0 else 0

    # -------------------------
    # Suspicious TLD
    # -------------------------
    suspicious_tlds = ["xyz", "top", "ru", "tk", "ml", "click", "gq", "cf"]
    tld = parts[-1] if len(parts) > 0 else ""
    features["SuspiciousTLD"] = 1 if tld in suspicious_tlds else 0

    return features