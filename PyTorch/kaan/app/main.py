from fastapi import FastAPI
from app.routers import upload
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
app.include_router(upload.router)

@app.get("/")
def root():
    return {"message": "Welcome to model upload mechanism"}
