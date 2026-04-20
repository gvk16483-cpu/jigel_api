import requests
import json

print("Testing Agent API directly...")
try:
    res = requests.post("http://127.0.0.1:8000/review", json={"query": "This is a test scam email with urgent link bit.ly/test"}, timeout=30)
    print(f"Status: {res.status_code}")
    print(f"Raw Response Text: {res.text}") 
    try:
        print(f"JSON Parsed: {json.dumps(res.json(), indent=2)}")
    except:
        print("Could not parse response as JSON")
except Exception as e:
    print(f"Error: {e}")
