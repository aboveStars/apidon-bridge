from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import pytorch, tensorflow #,keras

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(pytorch.router)
app.include_router(tensorflow.router)
#app.include_router(keras.router)


@app.get("/")
def root():
    return {"message": "Welcome to classify"}