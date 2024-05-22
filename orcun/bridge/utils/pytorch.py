from fastapi import FastAPI, Form, HTTPException
from PIL import Image
from io import BytesIO
import aiohttp
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn as nn
import json
import os
import aiofiles


async def load_labels_from_json(json_path):
    try:
        async with aiofiles.open(json_path, 'r') as file:
            contents = await file.read()
            labels_data = json.loads(contents)
        labels = labels_data['labels']
        num_classes = len(labels)
        return labels, num_classes
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Label file not found at {json_path}.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading labels from JSON at {json_path}: {str(e)}")



async def initialize_model(json_path):
    try:
        labels, num_classes = await load_labels_from_json(json_path)
        model = models.resnet18(pretrained=False)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, num_classes)
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error : {e}")

async def classify(image_url: str = Form(...), 
                   model_path_url: str = Form(...),
                   top_k = 5
                   ):
    try:
        full_model_path = "/app/data" + model_path_url 
        full_labels_path = os.path.split(full_model_path)[0] + '/label.json'
        classes, num_classes = await load_labels_from_json(full_labels_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while loading model: {str(e)}")

    try:
        model = await initialize_model(full_labels_path)
        state_dict = torch.load(full_model_path, map_location=torch.device('cpu'))
        model.load_state_dict(state_dict)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model state dictionary not found.")
    
    model.eval()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail=f"Error downloading image: {response.reason}")

                image_data = await response.read()

        image = Image.open(BytesIO(image_data))
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
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=400, detail=f"Error downloading image: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")

    try:
        with torch.no_grad():
            output = model(image)
            probs, indices = torch.topk(output, top_k)
            probs = torch.nn.functional.softmax(probs, dim=1)
        
        top_predictions = []
        for i in range(top_k):
            top_predictions.append({
                "class_name": classes[indices[0][i].item()],
                "probability": probs[0][i].item() * 100
            })

        return {"top_predictions": top_predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing classification: {e}")