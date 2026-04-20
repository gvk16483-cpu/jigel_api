from flask import Flask, request, jsonify
from flask_cors import CORS
from detect import predict
import os
import sklearn 
import threading
import traceback
import time

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "clean_model.joblib")

@app.route("/predict", methods=["POST"])
def predict_email():
    start_time = time.time()
    data = request.json
    print(f"DEBUG: Received Data from Extension")
    
    subject = data.get("subject", "")
    body = data.get("body", "")
    sender = data.get("from", "") 
    if not sender: sender = data.get("sender", "")
    links = data.get("links", [])
    platform = data.get("platform", "unknown")

    text = f"{subject} {body}".strip()

    try:
        # ==========================================
        # 🔹 STEP 2: LOCAL ML MODEL DECISION
        # ==========================================
        result = predict(MODEL_PATH, text, sender)
        
        ml_score = result.get("final_score", 0)
        is_hard_scam = result.get("prediction", 0) == 1
        
        ml_risk_label = "safe"
        if ml_score > 0.8: ml_risk_label = "dangerous"
        elif ml_score > 0.4: ml_risk_label = "suspicious"
        if is_hard_scam and ml_risk_label == "safe": ml_risk_label = "suspicious"

        # Defaults
        final_risk_label = ml_risk_label
        final_score = ml_score
        # 🚨 MOFIFIED: Pure ML Explanation
        explanation = "Analysis based on Machine Learning Model." 
        agent_score = None
        detected_patterns = []

        # ==========================================
        # 🔹 STEP 3: ML MODEL DECISION (ONLY)
        # ==========================================
        # Using ML model prediction directly - no agent fallback
        print(f"✅ ML Decision: {ml_risk_label} ({ml_score})")

        # ==========================================
        # 🔹 STEP 4: FINAL DECISION (ML ONLY)
        # ==========================================
        # Final decision is purely from ML model
        final_risk_label = ml_risk_label
        final_score = ml_score

        # ==========================================
        # 🔹 STEP 5: RESPONSE FORMAT
        # ==========================================
        scan_response = {
            "risk_label": final_risk_label,
            "final_risk_label": final_risk_label,
            "final_score": float(final_score),
            "explanation": explanation,
            "ml_score": float(ml_score),
            "agent_score": None,
            "platform": platform,
            "detected_patterns": detected_patterns
        }
        
        print(f"Sent: {final_risk_label} ({final_score})")
        return jsonify(scan_response)

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": str(e), 
            "risk_label": "suspicious", 
            "explanation": f"System Error: {str(e)[:50]}"
        })

if __name__ == "__main__":
    print("Starting Flask Server...")
    threading.Thread(target=lambda: requests.post("http://127.0.0.1:8000/review", json={"query": "ping"}, timeout=1) if time.sleep(2) else None).start()
    app.run(port=5000, debug=True, use_reloader=False)
