from fastapi import FastAPI,HTTPException,Form
from fastapi.middleware.cors import CORSMiddleware
from bridge.utils import tensorflow
from bridge.utils import pytorch
from bridge.utils import upload_file
from bridge.utils import tensorflow_lite
from bridge.utils import pretrained_pytorch
import bridge.utils.pretrained_tensorflow as pretrained_tensorflow

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
        return await tensorflow.classify(image_url,model_path_url)
    elif model_extension ==".pth":
        return await pytorch.classify(image_url,model_path_url)
    elif model_extension ==".tflite":
        return await tensorflow_lite.classify(image_url,model_path_url)
    else:
        raise HTTPException(status_code=400, detail="Unsupported model ID, Please provide a valid model_id with .h5 or .pth or .tflite extension.")

@app.post("/upload_model")
async def upload_models(url:str = Form(...),path:str = Form(...)):
    try:    
        return await upload_file.process_file(url,path)
    except Exception as e:
        print(e)

@app.post("/pretrained_tensorflow_classify/")
async def tf_classify_image(image_url:str = Form(...)):
    try:
        predictions = await pretrained_tensorflow.combine_predictions(image_url)
        return {"Combined Predictions": predictions}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/pretrained_pytorch_classify")
async def pt_classify_image(image_url:str = Form(...)):
    try:
        predictions = await pretrained_pytorch.classify_image(image_url)
        return {"Combined Predictions": predictions}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))