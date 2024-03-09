from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.tensorflow import host_tfmodel
from models.pytorch import host_ptmodel
from upload_file_mechanism import upload_file
from models.tensorflow_lite import host_tflitemodel


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(upload_file.router)
app.include_router(host_tfmodel.router)
app.include_router(host_ptmodel.router)
app.include_router(host_tflitemodel.router)


@app.get("/")
def root():
    return {"message": "Welcome to APIDON"}


