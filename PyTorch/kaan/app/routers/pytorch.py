from fastapi import HTTPException
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import requests
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn as nn

classes = [
    "Mantled Howler",
    "Patas Monkey",
    "Bald Uakari",
    "Japanese Macaque",
    "Pygmy Marmoset",
    "White Headed Capuchin",
    "Silvery Marmoset",
    "Common Squirrel Monkey",
    "Black Headed Night Monkey",
    "Nilgiri Langur",
]

class ClassificationRequest(BaseModel):
    image_url: str
    model_path_url: str

def initialize_model(model_path_url, num_classes=10):
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    model_path = f"app/models/pytorch_models/{model_path_url}"

    try:
        state_dict = torch.load(model_path, map_location=torch.device('cpu'))
        model.load_state_dict(state_dict)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model file not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model loading failed: {str(e)}")

    model.eval()
    return model

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

def classify_image(image, model):
    if image is None:
        raise HTTPException(status_code=400, detail="Provided image is not valid.")

    with torch.no_grad():
        output = model(image)
        probs, indices = torch.topk(output, 5)
        probs = torch.nn.functional.softmax(probs, dim=1)

        top_predictions = []
        for i in range(5):
            top_predictions.append({
                "class_name": classes[indices[0][i].item()],
                "probability": probs[0][i].item() * 100
            })

        return top_predictions

async def classify(request: ClassificationRequest):
    image = preprocess_image(request.image_url)
    model = initialize_model(request.model_path_url)
    top_predictions = classify_image(image, model)
    return {"top_predictions": top_predictions}