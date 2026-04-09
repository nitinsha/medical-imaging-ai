# Medical Imaging AI Backend

⚠️ Research use only — not a medical device.

## Endpoints

- POST /predict — upload X-ray image
- GET /health — system health check

## Run BE

# Create virtual environment
cd m    
create venv in root folder and not inside mdeical_ai_api. 

# Activate it
source venv/bin/activate

# install dependencies
pip install -r medical_ai_api/requirements_local.txt

# Run BE server
cd medical_ai_api

python run.py (recommended)
or
uvicorn app.main:app --reload

8️⃣ How to Test the API
Swagger UI (BEST for teaching)
Open browser:
http://127.0.0.1:8000/docs
Click POST /predict
Upload an X-ray image
Click Execute
See JSON response


## Run FE

Ensure FastAPI is running
Run Streamlit UI (new terminal):
streamlit run streamlit_app.py
