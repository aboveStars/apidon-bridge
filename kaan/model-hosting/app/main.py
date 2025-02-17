from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .routers import tensorflow, pytorch, tensorflow_lite, upload
from fastapi.middleware.cors import CORSMiddleware
from .utilities.middleware import APIKeyMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(APIKeyMiddleware)
app.include_router(upload.router)

class ClassifyRequest(BaseModel):
    image_url: str
    model_path: str

@app.get("/")
def root():
    return {"message": "Greetings from Apidon API"}

@app.post("/classify")
async def classify(request: ClassifyRequest):
    if request.model_path.endswith('.h5'):
        return await tensorflow.classify(request)
    elif request.model_path.endswith('.pth'):
        return await pytorch.classify(request)
    elif request.model_path.endswith('.tflite'):
        return await tensorflow_lite.classify(request)
    else:
        raise HTTPException(status_code=400, detail="Unsupported model extension. Please provide a model path with .h5, .pth, or .tflite extension.")