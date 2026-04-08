import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Medical Imaging AI", page_icon="🩻")
st.title("🩻 Medical Imaging AI Assistant")
st.caption("**Research Use Only – Not a Medical Diagnosis**")

uploaded_file = st.file_uploader("Upload Chest X-ray Image", type=["jpg", "jpeg", "png"])

if uploaded_file and st.button("Analyze Image"):
    with st.spinner("Analyzing..."):
        try:
            response = requests.post(
                API_URL,
                files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                st.markdown(f"### 🩺 {data['severity']} likelihood of abnormality")
                col1, col2 = st.columns(2)
                col1.metric("Model Probability", f"{data['probability']:.2f}")
                col2.metric("Model Certainty", f"{data['confidence']:.2f}")
                st.info(data["message"])
            else:
                st.error(f"Backend error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()
st.warning("⚠️ This tool is a research prototype. It must NOT be used for clinical diagnosis or treatment decisions. Always consult a qualified radiologist or physician.")