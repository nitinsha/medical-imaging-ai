# app/main.py | FastAPI Application
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.inference import load_model, predict

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app = FastAPI(
    title="Medical Imaging AI Backend",
    description="Research-use-only AI diagnostic backend",
    version="1.0"
)


@app.on_event("startup")
def startup_event():
    """
    Load model once when server starts.
    """
    load_model()


@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Receives an image file and returns AI-assisted diagnosis.
    """
    filename = file.filename.lower()
    extension = filename.split(".")[-1]

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a JPG or PNG image."
        )

    try:
        image_bytes = await file.read()
        result = predict(image_bytes)
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to process image",
                "detail": str(e)
            }
        )


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": True
    }
