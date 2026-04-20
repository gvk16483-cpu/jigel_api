import requests
import json

URL = "http://127.0.0.1:5000/predict"

def test_case(name, payload):
    print(f"\n--- Testing {name} ---")
    try:
        response = requests.post(URL, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request Failed: {e}")

# 1. Safe Case (ML should return Safe immediately)
test_case("Safe Email", {
    "subject": "Team Meeting Notes",
    "body": "Here are the notes from today's meeting. See you tomorrow.",
    "from": "manager@company.com",
    "platform": "gmail"
})

# 2. Dangerous Case (ML Dangerous -> Agent Dangerous)
test_case("Dangerous Scam", {
    "subject": "URGENT: Account Suspended",
    "body": "Your bank account has been suspended. Click here instantly to verify: bit.ly/scam-link-123. If you don't act now you lose funds.",
    "from": "support@bank-security-alert.xyz",
    "links": ["http://bit.ly/scam-link-123"],
    "platform": "gmail"
})
