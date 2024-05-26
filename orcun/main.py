from fastapi import FastAPI,HTTPException,Form,Depends,Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, Form, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import os
from bridge.utils import tensorflow
from bridge.utils import pytorch
from bridge.utils import upload_file
from bridge.utils import tensorflow_lite
from bridge.utils import pretrained_pytorch
import bridge.utils.pretrained_tensorflow as pretrained_tensorflow
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mou = FastAPI()

# CORS Middleware settings
origins = ["*"]
mou.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_key_header = APIKeyHeader(name="Authorization")
valid_api_key = os.getenv("MY_API_KEY")

#  Function that validates API key
def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key != valid_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@mou.get("/")
def root():
    return {"message": "welcome to apidon"}

@mou.post("/classify")
async def classify(image_url: str = Form(...),
                   model_path_url: str = Form(...), 
                   model_extension: str = Form(...),
                   api_key:str = Depends(validate_api_key),
                   img_height:str = Form(...),
                   img_width:str = Form(...)
                   ):
    img_height = int(img_height)
    img_width = int(img_width)
    if model_extension == ".h5":
        return await tensorflow.classify(image_url, model_path_url,img_height,img_width)
    elif model_extension == ".pth":
        return await pytorch.classify(image_url, model_path_url)
    elif model_extension == ".tflite":
        return await tensorflow_lite.classify(image_url, model_path_url)
    else:
        raise HTTPException(status_code=400, detail="Unsupported model ID, Please provide a valid model_id with .h5 or .pth or .tflite extension.")

@mou.post("/upload_model")
async def upload_models(url: str = Form(...), path: str = Form(...), api_key: str = Depends(validate_api_key),label_url:str = Form(...)):
    try:
        return await upload_file.process_file(url, path,label_url)
    except Exception as e:
        logger.error("Exception in upload_models: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@mou.post("/pretrained_tensorflow_classify/")
async def tf_classify_image(image_url: str = Form(...), api_key: str = Depends(validate_api_key)):
    try:
        start_time = time.time()  # Fonksiyon başlangıç zamanını kaydet

        loop = asyncio.get_event_loop()
        predictions = await loop.run_in_executor(ThreadPoolExecutor(), pretrained_tensorflow.combine_predictions, image_url)

        end_time = time.time()  # Fonksiyon bitiş zamanını kaydet
        elapsed_time = end_time - start_time  # Geçen süreyi hesapla

        print(f"Predictions completed in {elapsed_time} seconds.")  # Geçen süreyi yazdır

        return predictions
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@mou.post("/pretrained_pytorch_classify")
async def pt_classify_image(image_url: str = Form(...), api_key: str = Depends(validate_api_key)):
    try:
        start_time = time.time()  # Fonksiyon başlangıç zamanını kaydet

        predictions = await pretrained_pytorch.perform_classification(image_url)

        end_time = time.time()  # Fonksiyon bitiş zamanını kaydet
        elapsed_time = end_time - start_time  # Geçen süreyi hesapla

        print(f"Predictions completed in {elapsed_time} seconds.")  # Geçen süreyi yazdır

        return predictions
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

     