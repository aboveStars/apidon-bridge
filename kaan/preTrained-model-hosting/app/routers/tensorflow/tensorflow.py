from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from keras.applications.resnet50 import ResNet50, preprocess_input as preprocess_resnet
from keras.applications.vgg16 import VGG16, preprocess_input as preprocess_vgg
from keras.applications.mobilenet import MobileNet, preprocess_input as preprocess_mobilenet
from keras.applications.nasnet import NASNetMobile, preprocess_input as preprocess_nasnet
from keras.applications.densenet import DenseNet201, preprocess_input as preprocess_densenet
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing import image
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import numpy as np


router = APIRouter(
    prefix="/classify",
    tags=['classify']
)
class ImageUrl(BaseModel):
    image_url: str

resnet_model = ResNet50(weights="imagenet")
vgg_model = VGG16(weights="imagenet")
mobilenet_model = MobileNet(weights="imagenet")
nasnet_model = NASNetMobile(weights="imagenet")  
densenet_model = DenseNet201(weights="imagenet")

def preprocess_image(img_data, model_name):
    try:
        img = Image.open(BytesIO(img_data))
        img = img.resize((224, 224))
    except UnidentifiedImageError:
        raise ValueError("The image could not be identified and processed.")

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    if model_name == "resnet":
        x = preprocess_resnet(x)
    elif model_name == "vgg":
        x = preprocess_vgg(x)
    elif model_name == "mobilenet":
        x = preprocess_mobilenet(x)
    elif model_name == "nasnet":
        x = preprocess_nasnet(x)
    elif model_name == "densenet":
        x = preprocess_densenet(x)

    return x

def predict_image(img_data, model, model_name):
    try:
        x = preprocess_image(img_data, model_name)
        preds = model.predict(x)
        return decode_predictions(preds, top=5)[0]
    except Exception as e:
        raise ValueError(f"Prediction failed: {str(e)}")

def combine_predictions(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img_data = response.content
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Image request failed: {str(e)}")

    all_preds = []
    for model, model_name in zip(
        [resnet_model, vgg_model, mobilenet_model, nasnet_model, densenet_model],
        ["resnet", "vgg", "mobilenet", "nasnet", "densenet"]
    ):
        try:
            preds = predict_image(img_data, model, model_name)
            all_preds.extend(preds)
        except ValueError as e:
            continue

    if not all_preds:
        raise HTTPException(status_code=500, detail="All model predictions failed.")

    combined_predictions = {}
    for _, label, score in all_preds:
        if label not in combined_predictions or score > combined_predictions[label]:
            combined_predictions[label] = score

    sorted_predictions = sorted(combined_predictions.items(), key=lambda item: item[1], reverse=True)[:6]
    formatted_predictions = [{"label": label, "score": f"{score:.2%}"} for label, score in sorted_predictions]

    return formatted_predictions

@router.post("/tfclassify/")
async def classify_image(request: ImageUrl):
    try:
        predictions = combine_predictions(request.image_url)
        return {"Predictions": predictions}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
