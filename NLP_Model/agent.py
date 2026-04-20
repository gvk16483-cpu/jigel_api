import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json
import traceback
import re

# -----------------------------
# Configuration
# -----------------------------
api_key = "AIzaSyCgPojiS8sBqEwiCfND5HpxkQMVphzp5Cw"
os.environ["GOOGLE_API_KEY"] = api_key
genai.configure(api_key=api_key)

# Use the model as requested by the user
MODEL_NAME = "gemini-3.1-flash-lite-preview" 

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(title="AI Scam Reviewer API")

# -----------------------------
# Models & Prompts
# -----------------------------

# EXPLICIT SCORING PROMPT
SYSTEM_PROMPT = """
Analyze content for Scam/Risk.
Output JSON ONLY.
Explanation must be concise but helpful (2-3 sentences).

SCORING RULES:
- If SAFE: Score MUST be between 0 and 15.
- If SUSPICIOUS: Score MUST be between 40 and 75.
- If DANGEROUS: Score MUST be between 80 and 100.

Format:
{
  "agent_risk_label": "safe" | "suspicious" | "dangerous", 
  "agent_score": <int>, 
  "explanation": "<reasoning>",
  "detected_patterns": ["Pattern1"]
}
"""

# Initialize Model with Generation Config for Speed
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_PROMPT,
    generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=8192,
        temperature=0.4
    )
)

class ReviewRequest(BaseModel):
    query: str

def extract_json(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match: return json.loads(match.group(0))
        
        cleaned = text.strip()
        if cleaned.startswith("```json"): cleaned = cleaned[7:]
        if cleaned.startswith("```"): cleaned = cleaned[3:]
        if cleaned.endswith("```"): cleaned = cleaned[:-3]
        return json.loads(cleaned.strip())
    except:
        return None

# -----------------------------
# Endpoints
# -----------------------------

@app.post("/review")
async def review_content(request: ReviewRequest):
    try:
        response = model.generate_content(request.query)
        if not response.parts:
            return {
                "agent_risk_label": "suspicious",
                "agent_score": 75,
                "explanation": "Safety Block (Potential Scam).",
                "detected_patterns": ["Safety Block"]
            }

        text_response = response.text.strip()
        print(f"DEBUG: Agent raw response: {text_response[:200]}...")

        response_json = extract_json(text_response)

        if response_json:
            return response_json
        else:
            return {
                "agent_risk_label": "suspicious",
                "agent_score": 50,
                "explanation": f"Format Error.",
                "detected_patterns": ["Format Error"]
            }

    except Exception as e:
        print(f"Agent Error: {e}")
        return {
            "error": str(e),
            "agent_risk_label": "suspicious", 
            "explanation": f"Agent Error: {str(e)[:50]}",
            "detected_patterns": ["Error"]
        }

if __name__ == "__main__":
    print(f"AI Agent (Gemini 2.5) running on port 8000...")
    try:
        model.generate_content("ping")
    except: pass
    uvicorn.run(app, host="127.0.0.1", port=8000)
