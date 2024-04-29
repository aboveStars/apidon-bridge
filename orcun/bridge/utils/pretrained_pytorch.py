from fastapi import FastAPI, HTTPException, Form
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydantic import BaseModel
import torch
from torchvision import models, transforms
from PIL import Image
import requests
from io import BytesIO
import json

app = FastAPI()

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

with open('/app/bridge/utils/imagenet_class_index.json') as f:
    idx2label = [labels[1] for labels in json.load(f).values()]

def classify_with_model(model_name, image_tensor):
    model = load_model(model_name)
    with torch.no_grad():
        out = model(image_tensor)
    probs = torch.nn.functional.softmax(out, dim=1)
    top_probs, top_classes = torch.topk(probs, 5)

    predictions = []
    for i in range(top_probs.size(1)):
        class_name = idx2label[top_classes[0][i]]
        prob = top_probs[0][i].item() * 100
        predictions.append((class_name, prob))

    return predictions

async def perform_classification(image_url):
    image_tensor = get_preprocessed_image_tensor(image_url)
    model_names = ['efficientnet_v2_s', 'convnext_tiny', 'swin_transformer_tiny', 'mobilenet_v2', 'resnet50']

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(classify_with_model, model_name, image_tensor) for model_name in model_names]
        all_predictions = [future.result() for future in as_completed(futures)]

    consolidated_predictions = {}
    for predictions, model_name in zip(all_predictions, model_names):
        for class_name, prob in predictions:
            if class_name not in consolidated_predictions or prob > consolidated_predictions[class_name][1]:
                consolidated_predictions[class_name] = (model_name, prob)

    sorted_predictions = sorted(consolidated_predictions.items(), key=lambda item: item[1][1], reverse=True)[:6]

    combined_predictions = [
        {"label": class_name, "score": f"{prob:.2f}%"} for class_name, (_, prob) in sorted_predictions
    ]

    return {"Combined Predictions": combined_predictions}
