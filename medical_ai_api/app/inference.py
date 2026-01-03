import tensorflow as tf
from app.utils import preprocess_image

MODEL_PATH = "model/final_cnn_xray_ui_ready.keras"

model = None


def load_model():
    """
    Loads the model once at application startup.
    """
    global model
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded successfully")


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
    if model is None:
        raise RuntimeError("Model is not loaded")

    image_tensor = preprocess_image(image_bytes)
    prob = float(model.predict(image_tensor)[0][0])

    result = interpret_prediction(prob)
    result["probability"] = round(prob, 3)

    return result
