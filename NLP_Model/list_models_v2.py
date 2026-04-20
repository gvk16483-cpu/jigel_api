from google import genai
import os

api_key = "AIzaSyD-ae0dRQTAvNIUK6gYpTU1mh6mKB7nogM"
os.environ["GOOGLE_API_KEY"] = api_key

print("Initializing google.genai.Client...")
try:
    client = genai.Client(api_key=api_key)
    print("Listing models via google.genai...")
    
    # google.genai has user-friendly methods, look for models.list or similar
    # The new SDK structure might be client.models.list()
    
    # Try multiple ways as SDK is new
    try:
        for m in client.models.list():
            print(f"Model: {m.name}")
    except Exception as e1:
        print(f"client.models.list failed: {e1}")
        
except Exception as e:
    print(f"Client init failed: {e}")
