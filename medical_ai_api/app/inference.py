import tensorflow as tf
from app.utils import preprocess_image
from pathlib import Path
import requests

model = None 
# MODEL_PATH = "model/final_cnn_xray_ui_ready.keras"
BASE_DIR = Path(__file__).resolve().parent.parent
LOCAL_MODEL_PATH = BASE_DIR / "model" / "final_cnn_xray_ui_ready.keras"

MODEL_URL = "https://pub-a9cb4eba4f5944d7aa1f92499de40c7e.r2.dev/final_cnn_xray_ui_ready.keras"

def download_model():
    LOCAL_MODEL_PATH.parent.mkdir(exist_ok=True)

    if not LOCAL_MODEL_PATH.exists():
        print("⬇️ Downloading model from R2...")

        with requests.get(MODEL_URL, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(LOCAL_MODEL_PATH, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print("✅ Model downloaded")

def load_model():
    global model
    download_model()
    model = tf.keras.models.load_model(LOCAL_MODEL_PATH)
    print("✅ Model loaded into memory")

def get_model():
    return model

def interpret_prediction(prob):
    """
    Converts raw probability into safe, human-readable output.
    """
    certainty = max(prob, 1 - prob)

    if certainty < 0.6:
        return {
            "severity": "UNCERTAIN",
            "confidence": round(certainty, 2),
            "message": "Low confidence – radiologist review required"
        }

    if prob >= 0.7:
        return {
            "severity": "HIGH",
            "confidence": round(certainty, 2),
            "message": "High likelihood of abnormality"
        }
    elif prob >= 0.5:
        return {
            "severity": "MODERATE",
            "confidence": round(certainty, 2),
            "message": "Possible abnormality detected"
        }
    else:
        return {
            "severity": "LOW",
            "confidence": round(certainty, 2),
            "message": "No strong abnormality detected"
        }


def predict(image_bytes):
    """
    Full inference pipeline:
    image bytes → tensor → model → interpreted output
    """
    model = get_model()
    if model is None:
        raise RuntimeError("Model is not loaded")

    image_tensor = preprocess_image(image_bytes)
    prob = float(model.predict(image_tensor)[0][0])

    result = interpret_prediction(prob)
    result["probability"] = round(prob, 3)

    return result
