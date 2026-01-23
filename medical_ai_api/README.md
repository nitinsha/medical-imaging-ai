# Medical Imaging AI Backend

⚠️ Research use only — not a medical device.

## Endpoints

- POST /predict — upload X-ray image
- GET /health — system health check

## Run BE

source venv/bin/activate
deactivate
uvicorn app.main:app --reload

## Run FE

Ensure FastAPI is running
Run Gradio UI (new terminal):
python gradio_app.py
