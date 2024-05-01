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
from concurrent.futures import ThreadPoolExecutor

router = APIRouter(
    prefix="/classify",
    tags=['classify']
)

class ImageUrl(BaseModel):
    image_url: str

models_dict = {
    "resnet": ResNet50(weights="imagenet"),
    "vgg": VGG16(weights="imagenet"),
    "mobilenet": MobileNet(weights="imagenet"),
    "nasnet": NASNetMobile(weights="imagenet"),
    "densenet": DenseNet201(weights="imagenet")
}

def preprocess_image(img_data, model_name):
    try:
        img = Image.open(BytesIO(img_data)).resize((224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        preprocess_functions = {
            "resnet": preprocess_resnet,
            "vgg": preprocess_vgg,
            "mobilenet": preprocess_mobilenet,
            "nasnet": preprocess_nasnet,
            "densenet": preprocess_densenet
        }
        x = preprocess_functions[model_name](x)
    except UnidentifiedImageError:
        raise ValueError("The image could not be identified and processed.")
    return x

def predict_image(img_data, model_name):
    try:
        model = models_dict[model_name]
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
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_model = {executor.submit(predict_image, img_data, model_name): model_name for model_name in models_dict.keys()}
        for future in future_to_model:
            try:
                preds = future.result()
                all_preds.extend(preds)
            except ValueError:
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
