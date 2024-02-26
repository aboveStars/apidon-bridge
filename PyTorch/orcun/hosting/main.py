from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.tensorflow import host_tfmodel
from .models.pytorch import host_ptmodel

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(host_tfmodel.router)
app.include_router(host_ptmodel.router)


@app.get("/")
def root():
    return {"message": "Welcome to APIDON"}