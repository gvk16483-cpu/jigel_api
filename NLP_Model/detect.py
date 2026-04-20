import argparse
import joblib
import re
import numpy as np
from urllib.parse import urlparse
import requests
import os

# ==============================
# REQUIRED FOR PICKLE LOADING
# ==============================

from features import structural_features
# ==============================
# CONFIGURATION
# ==============================

THRESHOLD = 0.50

SUSPICIOUS_DOMAINS = [
    "forms.gle",
    "bit.ly",
    "tinyurl",
    "t.me",
    "wa.me",
]

FREE_EMAIL_PROVIDERS = [
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "protonmail.com"
]

SUSPICIOUS_TLDS = [
    ".xyz",
    ".top",
    ".online",
    ".info",
    ".site"
]

# ==============================
# GLOBAL MODEL CACHE
# ==============================
_GLOBAL_MODEL = None

def get_model(model_path):
    global _GLOBAL_MODEL
    if _GLOBAL_MODEL is None:
        if os.path.exists(model_path):
            print(f"Loading model from {model_path}...")
            _GLOBAL_MODEL = joblib.load(model_path)
        else:
            print(f"Error: Model file not found at {model_path}")
            return None
    return _GLOBAL_MODEL

# ==============================
# LINK RISK SCORE
# ==============================

def link_risk_score(text):
    urls = re.findall(r'http[s]?://\S+', text.lower())
    if not urls:
        return 0.0

    suspicious = 0

    for url in urls:
        parsed = urlparse(url)
        host = parsed.netloc

        if any(domain in host for domain in SUSPICIOUS_DOMAINS):
            suspicious += 1

        if re.search(r'\d+\.\d+\.\d+\.\d+', host):
            suspicious += 1

    return suspicious / len(urls)


# ==============================
# MANIPULATION SCORE
# ==============================

def manipulation_score(text):
    text = text.lower()

    urgency = len(re.findall(r'urgent|immediate|final|limited|act now|deadline|expire|last chance|registration link|apply now', text))
    reward = len(re.findall(r'prize|cash|reward|profit|earn|bonus|investment|payment|tablet|internship|training|stipend|scholarship|referral|fee', text))
    authority = len(re.findall(r'government|bank|rbi|court|income tax|aicte|ministry|nasscom|official|admin|capgemini|inspire leap|hr|hiring', text))

    return min((urgency + reward + authority) / 10, 1.0)


# ==============================
# SENDER RISK SCORE
# ==============================

def sender_risk_score(sender, text):
    if not sender:
        return 0.0

    sender = sender.lower()

    if "@" not in sender:
        return 0.3

    domain = sender.split("@")[-1]
    risk = 0.0

    if domain in FREE_EMAIL_PROVIDERS:
        if re.search(r'accenture|ibm|microsoft|bank|government|aicte|internship', text.lower()):
            risk += 0.6
        else:
            risk += 0.3

    if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS):
        risk += 0.4

    if len(re.findall(r'\d', domain)) >= 4:
        risk += 0.3

    return min(risk, 1.0)


# ==============================
# MAIN PREDICTION FUNCTION
# ==============================

def predict(model_path, text, sender=None):
    # Use cached model
    model = get_model(model_path)
    
    if model is None:
        # Fallback if model load failed
        return {
            "ml_probability": 0.5,
            "final_score": 0.5,
            "prediction": 0,
            "error": "Model not found"
        }

    ml_prob = model.predict_proba([text])[0][1]

    # SCORING COMPONENTS (Calculated but NOT used for final score)
    link_score = link_risk_score(text)
    manip_score = manipulation_score(text)
    sender_score = sender_risk_score(sender, text)

    # 🚨 PURE ML MODE (User Request: "No patterns")
    # We ignore link_score, manip_score, sender_score for the final decision.
    final_score = ml_prob 

    # final_score = min(final_score, 1.0) # ml_prob is already 0-1
    final_prediction = 1 if final_score >= THRESHOLD else 0

    return {
        "ml_probability": ml_prob,
        "link_score": float(link_score),
        "manipulation_score": float(manip_score),
        "sender_score": float(sender_score),
        "final_score": float(final_score),
        "threshold": THRESHOLD,
        "prediction": final_prediction
    }


# ==============================
# CLI ENTRY
# ==============================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="model.joblib")
    parser.add_argument("--text", default="")
    parser.add_argument("--sender", default=None)
    args = parser.parse_args()

    result = predict(args.model, args.text, args.sender)
    print(result)

    # 🚨 IF SPAM → SEND TO AIAGENT
    if result["prediction"] == 1:
        print("\n⚠️ Spam detected. Sending content to AI Agent...")
        
        # NOTE: This part is for CLI testing only, not used by app.py
        try:
            with open("test_email.txt", "r", encoding="utf-8") as f:
                email_text = f.read()

            response = requests.post(
                "http://127.0.0.1:8000/review",
                json={"query": email_text}
            )

            print("\n🧠 AI Agent Analysis:")
            print(response.json())
        except Exception as e:
            print(f"Error calling agent from CLI: {e}")