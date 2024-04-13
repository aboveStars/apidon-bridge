from fastapi import FastAPI
from .routers.tensorflow import tensorflow
from .routers.pytorch import pytorch
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

@app.get("/")
def root():
    return {"message": "Greetings from Apidon API"}
