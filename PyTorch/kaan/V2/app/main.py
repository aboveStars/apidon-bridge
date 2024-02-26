from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .routers import tensorflow, pytorch  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tensorflow.router)
app.include_router(pytorch.router)

class ClassifyRequest(BaseModel):
    image_url: str
    id_model: str

@app.get("/")
def root():
    return {"message": "Welcome to classify"}

@app.post("/classify")
async def classify(request: ClassifyRequest):

    if request.id_model.endswith('.h5'):

        return await tensorflow.classify(request)
    elif request.id_model.endswith('.pth'):

        return await pytorch.classify(request)
    else:
        raise HTTPException(status_code=400, detail="Unsupported model ID. Please provide a valid model_id with .h5 or .pth extension.")
