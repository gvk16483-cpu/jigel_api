import os
from detect import predict
import requests
import json

# Email Data from User
subject = "VNR VJIET – Skill Development & Stipend-Based Online Training & Internship Program 2026SAFE"
sender = "vtu19258@veltech.edu.in"
body = """Dear Student Of VNR VJIET

Aenexz Tech is excited to introduce the Stipend-Based Online Training & Internship Program 2026 exclusively for VNR VJIET in association with leading MNCs like IBM, Microsoft, and Wipro.

Program Benefits Included in Your Enrollment
Month 1 – Core Technical Training
Structured alternate-day classes

Theory + practical learning

Hands-on training with industry-relevant tools and technologies

Month 2 – Real-Time Industry Project
Work on a live company project

Weekly mentor support

Build a portfolio-ready project

Month 3 – Placement & Stipend Opportunities
Performance-based stipend: ₹15,000 – ₹25,000

Interview opportunities with hiring partners

Resume & LinkedIn enhancement

HR screening and interview preparation 

Registration Form: https://forms.gle/Registration-form
Certifications You Will Receive
Training Completion Certificate

Internship Completion Certificate

Letter of Experience (LOE)

Letter of Recommendation (LOR) for top performers

All certificates are AICTE, ISO, and MSME recognized, adding strong value to your professional profile.

Registration Form: https://forms.gle/Registration-form

It is mandatory to fill this form to receive official updates and program-related information.
Best Regards,
AENEXZ TECH"""

links = ["https://forms.gle/Registration-form"]
text = f"{subject} {body}".strip()
model_path = "clean_model.joblib"

print("--- 1. Testing Raw ML Model (detect.py) ---")
try:
    result = predict(model_path, text, sender)
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"ML Prediction Failed: {e}")

print("\n--- 2. Testing API Workflow (app.py) ---")
payload = {
    "subject": subject,
    "from": sender,
    "body": body,
    "links": links,
    "platform": "gmail"
}
try:
    res = requests.post("http://127.0.0.1:5000/predict", json=payload, timeout=30)
    print(f"Status: {res.status_code}")
    print(json.dumps(res.json(), indent=2))
except Exception as e:
    print(f"API Request Failed: {e}")
