from fastapi import FastAPI
from pydantic import BaseModel
from .routers import tensorflow
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

class ClassifyRequest(BaseModel):
    image_url: str
    model_path_url: str

@app.get("/")
def root():
    return {"message": "Greetings from Apidon API"}
