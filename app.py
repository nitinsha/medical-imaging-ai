import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# -----------------------------
# CONFIG
# -----------------------------
MODEL_PATH = "medical_ai_api/model/final_cnn_xray_ui_ready.keras"
IMG_SIZE = (224, 224)

# -----------------------------
# Load model ONCE at startup
# -----------------------------
model = tf.keras.models.load_model(MODEL_PATH)

# -----------------------------
# Inference + Interpretation
# -----------------------------
def interpret_prediction(prob):
    """
    Converts raw probability into human-readable output.
    """
    confidence = max(prob, 1 - prob)

    if confidence < 0.6:
        return "UNCERTAIN", confidence, "Low confidence – radiologist review required"

    if prob >= 0.7:
        return "HIGH", confidence, "High likelihood of abnormality"
    else:
        return "LOW", confidence, "No strong abnormality detected"


def analyze_image(image: Image.Image):
    """
    Gradio callback: image → model → interpretation
    """
    if image is None:
        return "No image uploaded", "", "", ""

    # --- Preprocessing (MUST match training) ---
    img = image.convert("RGB")
    img = img.resize(IMG_SIZE)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # --- Prediction ---
    prob = float(model.predict(img_array)[0][0])

    # --- Interpretation ---
    severity, confidence, message = interpret_prediction(prob)

    return (
        f"🩺 **{severity} likelihood of abnormality**",
        f"{prob:.2f}",
        f"{confidence:.2f}",
        message
    )

# -----------------------------
# Gradio UI
# -----------------------------
with gr.Blocks(title="Medical Imaging AI – Research Demo") as demo:

    gr.Markdown("""
    # 🩻 Medical Imaging AI Assistant  
    **Research Use Only – Not a Medical Diagnosis**

    Upload a chest X-ray image to receive an AI-assisted assessment.
    """)

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(
                type="pil",
                label="Upload Chest X-ray Image"
            )
            analyze_btn = gr.Button("Analyze Image")

        with gr.Column():
            finding_output = gr.Markdown(label="Primary Finding")
            probability_output = gr.Textbox(label="Model Probability")
            confidence_output = gr.Textbox(label="Model Certainty")
            message_output = gr.Textbox(label="Explanation")

    gr.Markdown("""
    ---
    ⚠️ **Disclaimer**  
    This tool is a research prototype.  
    It must NOT be used for clinical diagnosis or treatment decisions.  
    Always consult a qualified radiologist or physician.
    """)

    analyze_btn.click(
        fn=analyze_image,
        inputs=image_input,
        outputs=[
            finding_output,
            probability_output,
            confidence_output,
            message_output
        ]
    )

# -----------------------------
# Entry point for HF Spaces
# -----------------------------
if __name__ == "__main__":
    demo.launch()
