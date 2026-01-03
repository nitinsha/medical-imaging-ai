# Medical Imaging AI Backend

⚠️ Research use only — not a medical device.

## Endpoints

- POST /predict — upload X-ray image
- GET /health — system health check

## create a virtual environment.

Step 1 — Create a virtual environment (one-time)
From your project root (medical_ai_api/):
python3 -m venv venv
This creates a local isolated Python environment.
Step 2 — Activate the virtual environment
On macOS / Linux:
(After restarting your laptop, you must Reactivate the virtual environment using same command)
source venv/bin/activate
On Windows:
venv\Scripts\activate
After activation, your terminal prompt will change to:
(venv) your-name@machine medical_ai_api %
This confirms you are inside the virtual environment.
Step 3 — Install dependencies safely
Now run:
pip install -r requirements.txt
All packages will be installed only for this project.
Step 4 — Tell VS Code to use this Python interpreter (important)
In VS Code:
Press Cmd + Shift + P (or Ctrl + Shift + P)
Select “Python: Select Interpreter”

Choose the interpreter inside:
medical_ai_api/venv/bin/python

## Usage

# How to Run & Test Locally (Step-by-Step)

Step 1 — Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

Step 2 — Install dependencies
pip install -r requirements.txt

Step 3 — Start FastAPI server: (make sure to be inside medical_ai_api folder before running cmd)
uvicorn app.main:app --reload

Expected output:
Uvicorn running on http://127.0.0.1:8000
Model loaded successfully

8️⃣ How to Test the API
Option 1 — Swagger UI (BEST for teaching)
Open browser:
http://127.0.0.1:8000/docs
Click POST /predict
Upload an X-ray image
Click Execute
See JSON response

Option 2 — Health Check
http://127.0.0.1:8000/health

Expected:
{"status":"ok","model_loaded":true}

✅ GRADIO UI
Create this file at the project root
MIDS/
├── medical_ai_api/
├── gradio_app.py ← THIS FILE

2️⃣ Install Gradio (inside your venv)
Make sure your virtual environment is active:
source venv/bin/activate

Then install Gradio:
pip install gradio requests

4️⃣ How to Run the Gradio UI Locally
Step 1 — Ensure FastAPI is running
In one terminal:
uvicorn app.main:app --reload
Confirm:
http://127.0.0.1:8000/docs works
Step 2 — Run Gradio UI (new terminal)
python gradio_app.py
Expected output:
Running on local URL: http://127.0.0.1:7860
Open browser:
http://127.0.0.1:7860

How to exit the virtual environment
In your terminal, just run:
deactivate

## Step-by-step: Fix using Git LFS

Step 1 — Install Git LFS (one-time)
brew install git-lfs
Verify:
git lfs version
Step 2 — Initialize Git LFS in this repo
From project root:
git lfs install
Step 3 — Tell Git LFS to track .keras files
git lfs track "_.keras"
git lfs track "\*.keras" (remove \)
This creates/updates .gitattributes.
Verify:
cat .gitattributes
You should see:
_.keras filter=lfs diff=lfs merge=lfs -text
Step 4 — Remove the model from normal Git tracking
This step is critical.
git rm --cached medical_ai_api/model/final_cnn_xray_ui_ready.keras

⚠️ This does NOT delete the file locally.
Step 5 — Re-add the model via LFS
git add medical_ai_api/model/final_cnn_xray_ui_ready.keras

Step 6 — Commit LFS changes
git add .gitattributes
git commit -m "Track Keras model with Git LFS"

Verify LFS tracking (DO NOT SKIP)
git lfs ls-files
You must see:
medical_ai_api/model/final_cnn_xray_ui_ready.keras

Step 7 — Push again (this WILL work)
git push -u origin main

You will now see:
Git pushes code normally
Model is uploaded via LFS
No size error
