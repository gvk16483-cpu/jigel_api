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

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from features import structural_features  # noqa: F401 - required for joblib model loading
    from detect import predict as ml_predict
    IMPORT_ERROR = None
except ImportError as e:
    print(f"Import error: {e}. Using fallback detection.")
    ml_predict = None
    IMPORT_ERROR = str(e)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Model configuration
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "clean_model.joblib")

# Global model cache
_GLOBAL_MODEL = None


def get_model(model_path):
    """Load or retrieve cached model."""
    global _GLOBAL_MODEL
    if _GLOBAL_MODEL is None:
        try:
            _GLOBAL_MODEL = joblib.load(model_path)
            print(f"[VERCEL] Model loaded: {model_path}")
        except Exception as e:
            print(f"[VERCEL] Model load failed: {e}")
            _GLOBAL_MODEL = None
    return _GLOBAL_MODEL


def get_runtime_status():
    model_exists = os.path.exists(MODEL_PATH)
    model = get_model(MODEL_PATH) if model_exists else None
    return {
        "import_ok": ml_predict is not None,
        "import_error": IMPORT_ERROR,
        "model_path": MODEL_PATH,
        "model_exists": model_exists,
        "model_loaded": model is not None,
    }


@app.route('/predict', methods=['POST'])
@app.route('/api/predict', methods=['POST'])
def predict_email():
    """
    Main prediction endpoint for fraud detection.

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
        print("[VERCEL] Received prediction request")

        subject = data.get("subject", "")
        body = data.get("body", "")
        sender = data.get("from") or data.get("sender", "")
        platform = data.get("platform", "unknown")

        text = f"{subject} {body}".strip()

        runtime_status = get_runtime_status()
        if not runtime_status["import_ok"] or not runtime_status["model_loaded"]:
            print(f"[VERCEL] ML runtime unavailable: {runtime_status}")
            return jsonify({
                "error": "ML runtime unavailable",
                "risk_label": "error",
                "final_risk_label": "error",
                "final_score": 0.0,
                "explanation": "Deployed model is unavailable. Check Vercel imports and model file packaging.",
                "platform": platform,
                "runtime_status": runtime_status
            }), 503

        result = ml_predict(MODEL_PATH, text, sender)

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
            ml_score = 0.0
            ml_risk_label = "error"

        scan_response = {
            "risk_label": ml_risk_label,
            "final_risk_label": ml_risk_label,
            "final_score": float(ml_score),
            "explanation": "Analysis based on Machine Learning Model.",
            "ml_score": float(ml_score),
            "agent_score": None,
            "platform": platform,
            "detected_patterns": [],
            "processing_time_ms": int((time.time() - start_time) * 1000)
        }

        print(f"[VERCEL] Result: {ml_risk_label} ({ml_score:.2f})")
        return jsonify(scan_response), 200

    except Exception as e:
        print(f"[VERCEL] Error: {e}")
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
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Fraud Detection API",
        "timestamp": time.time(),
        "runtime_status": get_runtime_status()
    }), 200


@app.route('/', methods=['GET'])
def index():
    """Root endpoint."""
    return jsonify({
        "service": "Fraud Detection API",
        "version": "2.1",
        "endpoints": {
            "predict": "/predict (POST) or /api/predict (POST)",
            "health": "/health (GET) or /api/health (GET)"
        }
    }), 200


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


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "error": "Internal server error",
        "message": str(e)
    }), 500


if __name__ != "__main__":
    pass


if __name__ == "__main__":
    print("Starting Fraud Detection API...")
    app.run(debug=False, host='0.0.0.0', port=5000)
