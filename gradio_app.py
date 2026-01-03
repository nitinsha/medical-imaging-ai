import gradio as gr
import requests
import tempfile
import os

# 🔧 CONFIG
API_URL = "http://127.0.0.1:8000/predict"  # FastAPI backend
SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png")


def analyze_image(image):
    """
    Sends image to FastAPI backend and returns formatted results.
    """
    if image is None:
        return "No image uploaded.", "", "", ""

    # Save image temporarily
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        image.save(tmp.name)
        temp_path = tmp.name

    try:
        with open(temp_path, "rb") as f:
            response = requests.post(
                API_URL,
                files={"file": f},
                timeout=30
            )

        if response.status_code != 200:
            return (
                "❌ Error",
                "",
                "",
                response.json().get("detail", "Backend error")
            )

        data = response.json()

        finding = f"🩺 **{data['severity']} likelihood of abnormality**"
        probability = f"{data['probability']:.2f}"
        confidence = f"{data['confidence']:.2f}"
        message = data["message"]

        return finding, probability, confidence, message

    except Exception as e:
        return "❌ Error", "", "", str(e)

    finally:
        os.remove(temp_path)


# 🎨 GRADIO UI
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

if __name__ == "__main__":
    demo.launch()
