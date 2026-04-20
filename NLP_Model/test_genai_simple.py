import google.generativeai as genai
import os

api_key = "AIzaSyDJjISmPUApUMCb9lPm3STSp3YibPw0FX4"
genai.configure(api_key=api_key)

print("--- Listing Details ---")
try:
    for m in genai.list_models():
        if "gemini" in m.name:
            print(f"Model: {m.name}")
            print(f"Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"List failed: {e}")

print("\n--- Testing gemini-pro ---")
try:
    model = genai.GenerativeModel("gemini-pro")
    res = model.generate_content("Hello")
    print(f"Success: {res.text}")
except Exception as e:
    print(f"Failed: {e}")
