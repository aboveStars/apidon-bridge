from fastapi import HTTPException
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import requests
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn as nn
import json
import os

class ClassificationRequest(BaseModel):
    image_url: str
    model_path: str

def load_labels_from_json(json_path):
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            labels = data['labels']
        return labels
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Label file not found at {json_path}.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading labels from JSON at {json_path}: {str(e)}")

def initialize_model(model_path, num_classes=None):
    normalized_model_path = '/' + model_path.strip('/')

    full_model_path = f'/app/data{normalized_model_path}'
    full_labels_path = os.path.splitext(full_model_path)[0] + '.json'

    try:
        labels = load_labels_from_json(full_labels_path)
    except HTTPException as e:
        raise e

    num_classes = len(labels)

    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)

    try:
        state_dict = torch.load(full_model_path, map_location=torch.device('cpu'))
        model.load_state_dict(state_dict)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Model file not found at {full_model_path}.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model loading failed from {full_model_path}: {str(e)}")

    model.eval()
    return model, labels

def preprocess_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        if image.mode != 'RGB':
            image = image.convert('RGB')

        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]

        image_transforms = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean, std)
        ])

        image = image_transforms(image).unsqueeze(0)
        return image

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error downloading image: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")

def classify_image(image, model, labels):
    if image is None:
        raise HTTPException(status_code=400, detail="Provided image is not valid.")

    with torch.no_grad():
        output = model(image)
        probs, indices = torch.topk(output, 5)
        probs = torch.nn.functional.softmax(probs, dim=1)

        top_predictions = []
        for i in range(5):
            top_predictions.append({
                "label": labels[indices[0][i].item()],
                "score": probs[0][i].item() * 100
            })

        return top_predictions

async def classify(request: ClassificationRequest):
    image = preprocess_image(request.image_url)
    model, labels = initialize_model(request.model_path)
    top_predictions = classify_image(image, model, labels)
    return {"predictions": top_predictions}
