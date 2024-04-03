from fastapi import FastAPI,HTTPException,Form
from fastapi.middleware.cors import CORSMiddleware
from bridge.utils import host_tfmodel
from bridge.utils import host_ptmodel
from bridge.utils import upload_file
from bridge.utils import host_tflitemodel

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/")
def root():
    return {"message": "Welcome to APIDON"}


@app.post("/classify")
async def classify(image_url:str = Form(...),model_path_url:str = Form(...),model_extension : str = Form(...)):
    if model_extension == ".h5":
        return await host_tfmodel.classify(image_url,model_path_url)
    elif model_extension ==".pth":
        return await host_ptmodel.classify(image_url,model_path_url)
    elif model_extension ==".tflite":
        return await host_tflitemodel.classify(image_url,model_path_url)
    else:
        raise HTTPException(status_code=400, detail="Unsupported model ID. Please provide a valid model_id with .h5 or .pth or .tflite extension.")

@app.post("/upload_model")
async def upload_models(url:str = Form(...),path:str = Form(...)):
    try:    
        return await upload_file.process_file(url,path)
    except Exception as e:
        print(e)


