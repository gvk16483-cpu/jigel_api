"""
Vercel Serverless API - Fraud Detection ML Model
Deployed to: https://your-app.vercel.app/api/predict
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import traceback
import time
import joblib
import numpy as np
from urllib.parse import urlparse

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from features import structural_features
    from detect import predict as ml_predict
except ImportError as e:
    print(f"Import error: {e}. Using fallback detection.")
    ml_predict = None

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Model configuration
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "clean_model.joblib")

# Global model cache
_GLOBAL_MODEL = None

def get_model(model_path):
    """Load or retrieve cached model"""
    global _GLOBAL_MODEL
    if _GLOBAL_MODEL is None:
        try:
            _GLOBAL_MODEL = joblib.load(model_path)
            print(f"✅ Model loaded: {model_path}")
        except Exception as e:
            print(f"❌ Model load failed: {e}")
            _GLOBAL_MODEL = None
    return _GLOBAL_MODEL

@app.route('/predict', methods=['POST'])
@app.route('/api/predict', methods=['POST'])
def predict_email():
    """
    Main prediction endpoint for fraud detection
    
    Request JSON:
    {
        "subject": "Email subject",
        "body": "Email body",
        "from": "sender@email.com",
        "links": ["url1", "url2"],
        "platform": "gmail" | "whatsapp" | "telegram"
    }
    """
    start_time = time.time()
    
    try:
        data = request.json or {}
        print(f"[VERCEL] Received prediction request")
        
        # Extract fields
        subject = data.get("subject", "")
        body = data.get("body", "")
        sender = data.get("from") or data.get("sender", "")
        links = data.get("links", [])
        platform = data.get("platform", "unknown")

        # Combine text for analysis
        text = f"{subject} {body}".strip()

        # ==========================================
        # 🔹 ML MODEL DECISION (ONLY)
        # ==========================================
        
        # Use the detect.predict function
        result = ml_predict(MODEL_PATH, text, sender) if ml_predict else None
        
        if result:
            ml_score = result.get("final_score", 0.0)
            is_hard_scam = result.get("prediction", 0) == 1
            
            ml_risk_label = "safe"
            if ml_score > 0.8:
                ml_risk_label = "dangerous"
            elif ml_score > 0.4:
                ml_risk_label = "suspicious"
            if is_hard_scam and ml_risk_label == "safe":
                ml_risk_label = "suspicious"
        else:
            # Fallback if model unavailable
            ml_score = 0.0
            ml_risk_label = "safe"

        # Final decision is purely from ML model
        final_risk_label = ml_risk_label
        final_score = ml_score
        explanation = "Analysis based on Machine Learning Model."
        detected_patterns = []

        # ==========================================
        # 🔹 RESPONSE FORMATTING
        # ==========================================
        
        scan_response = {
            "risk_label": final_risk_label,
            "final_risk_label": final_risk_label,
            "final_score": float(final_score),
            "explanation": explanation,
            "ml_score": float(ml_score),
            "agent_score": None,
            "platform": platform,
            "detected_patterns": detected_patterns,
            "processing_time_ms": int((time.time() - start_time) * 1000)
        }
        
        print(f"[VERCEL] ✅ Result: {final_risk_label} ({final_score:.2f})")
        return jsonify(scan_response), 200

    except Exception as e:
        print(f"[VERCEL] ❌ Error: {e}")
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "risk_label": "error",
            "final_risk_label": "error",
            "final_score": 0.0,
            "explanation": f"System Error: {str(e)[:50]}",
            "platform": data.get("platform", "unknown") if 'data' in locals() else "unknown"
        }), 500

@app.route('/health', methods=['GET'])
@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Fraud Detection API",
        "timestamp": time.time()
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "service": "Fraud Detection API",
        "version": "2.0",
        "endpoints": {
            "predict": "/predict (POST) or /api/predict (POST)",
            "health": "/health (GET) or /api/health (GET)"
        }
    }), 200

# Error handler for 404
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": {
            "predict": "/predict or /api/predict",
            "health": "/health or /api/health",
            "root": "/"
        }
    }), 404

# Error handler for 500
@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "error": "Internal server error",
        "message": str(e)
    }), 500

# For WSGI compatibility with Vercel
if __name__ != "__main__":
    # This runs when deployed on Vercel
    pass

if __name__ == "__main__":
    # For local development
    print("Starting Fraud Detection API...")
    app.run(debug=False, host='0.0.0.0', port=5000)
