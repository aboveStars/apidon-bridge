from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import torch
from torchvision import models, transforms
from PIL import Image
import requests
from io import BytesIO
import json

router = APIRouter(
    prefix="/classify",
    tags=['classify']
)

class ImageUrl(BaseModel):
    image_url: str

def get_preprocessed_image_tensor(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img_t = preprocess(img)
    batch_t = torch.unsqueeze(img_t, 0)
    return batch_t

def load_model(model_name):
    model_dict = {
        'efficientnet_v2_s': models.efficientnet_v2_s,
        'convnext_tiny': models.convnext_tiny,
        'swin_transformer_tiny': models.swin_t,
        'mobilenet_v2': models.mobilenet_v2,
        'resnet50': models.resnet50
    }
    model_func = model_dict.get(model_name)
    if model_func is None:
        raise ValueError("Unsupported model")
    model = model_func(pretrained=True)
    model.eval()
    return model

with open('app/routers/pytorch/imagenet_class_index.json') as f:
    idx2label = [labels[1] for labels in json.load(f).values()]

async def perform_classification(image_url):
    image_tensor = get_preprocessed_image_tensor(image_url)
    model_names = ['efficientnet_v2_s', 'convnext_tiny', 'swin_transformer_tiny', 'mobilenet_v2', 'resnet50']
    
    consolidated_predictions = {}
    
    for model_name in model_names:
        model = load_model(model_name)
        with torch.no_grad():
            out = model(image_tensor)
        probs = torch.nn.functional.softmax(out, dim=1)
        top_probs, top_classes = torch.topk(probs, 5)
        
        for i in range(top_probs.size(1)):
            class_name = idx2label[top_classes[0][i]]
            prob = top_probs[0][i].item() * 100
            if class_name not in consolidated_predictions or prob > consolidated_predictions[class_name][1]:
                consolidated_predictions[class_name] = (model_name, prob)
                
    sorted_predictions = sorted(consolidated_predictions.items(), key=lambda item: item[1][1], reverse=True)[:6]
    
    formatted_predictions = [
        {"label": class_name, "score": f"{prob:.2f}%"} for class_name, (model_name, prob) in sorted_predictions
    ]
    
    return {"Predictions": formatted_predictions}

@router.post("/ptclassify/")
async def classify_image(image_data: ImageUrl):
    try:
        results = await perform_classification(image_data.image_url)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))