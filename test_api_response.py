import requests
import json

url = "http://127.0.0.1:5000/predict"
payload = {
    "subject": "Test Scam",
    "body": "Urgent: Click here to claim your prize from Aenexz Tech",
    "from": "test@example.com",
    "links": [],
    "platform": "gmail"
}

print("Testing API endpoint...")
try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
