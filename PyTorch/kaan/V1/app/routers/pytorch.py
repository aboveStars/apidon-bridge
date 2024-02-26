from fastapi import APIRouter
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import requests
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn as nn

router = APIRouter(
    prefix="/pytorch",
    tags=['PyTorch Model']
)

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

class ImageURL(BaseModel):
    image_url: str

class ClassificationResult(BaseModel):
    top_predictions: list[dict]


def initialize_model(model_path, num_classes=10):
    model = models.resnet18(pretrained=False)  
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)

    try:
        state_dict = torch.load(model_path)
        model.load_state_dict(state_dict)
    except FileNotFoundError:
        print("Error: Model state dictionary not found.")
        return None  

    model.eval()
    return model

model = initialize_model("models/pytorch_models/model_23.pth")

def preprocess_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  

        image = Image.open(BytesIO(response.content))
        if image.mode != 'RGB':
            image = image.convert('RGB')  

        mean = [0.4363, 0.4328, 0.3291]
        std = [0.2129, 0.2075, 0.2038]

        image_transforms = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(torch.Tensor(mean), torch.Tensor(std))
        ])

        image = image_transforms(image).unsqueeze(0)  
        return image

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None  
    except Exception as e:
        print(f"Error processing image: {e}")
        return None  

def classify_image(image):
    if image is None:
        return None  

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

@router.post("/classify/pytorch")
async def classify(image_url: ImageURL):
    try:
        image = preprocess_image(image_url.image_url)
        if image is None:
            return {"error": "Error processing image. Please make sure the URL is valid and points to a reachable image."}

        top_predictions = classify_image(image)
        if top_predictions is None:
            return {"error": "Error performing classification."}

        return {"top_predictions": top_predictions}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}