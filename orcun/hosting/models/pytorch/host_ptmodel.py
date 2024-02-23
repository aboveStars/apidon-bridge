from fastapi import Form,APIRouter
from PIL import Image
from io import BytesIO
import requests
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn as nn

# Define app and input/output models

router = APIRouter(
    prefix="/pytorch",
    tags=['pytorch']
)

model_path = 'hosting/models/pytorch/model_23.pth'

@router.get("/")
def root():
    return{"message":"This is the PyTorch model."}


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





# Model loading and initialization (place in a separate module for better organization)
def initialize_model(model_path, num_classes=10):
    model = models.resnet18(pretrained=False)  # pretrained=False for custom weights
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)

    # Load state dictionary (error handling and logging recommended)
    try:
        state_dict = torch.load(model_path)
        model.load_state_dict(state_dict)
    except FileNotFoundError:
        print("Error: Model state dictionary not found.")
        return None  # Handle errors gracefully

    model.eval()
    return model

model = initialize_model(model_path)  # Replace with your actual path

# Define image preprocessing function (considering feedback)
def preprocess_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise error for non-200 status codes

        image = Image.open(BytesIO(response.content))
        if image.mode != 'RGB':
            image = image.convert('RGB')  # Ensure RGB format

        mean = [0.4363, 0.4328, 0.3291]
        std = [0.2129, 0.2075, 0.2038]

        image_transforms = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(torch.Tensor(mean), torch.Tensor(std))
        ])

        image = image_transforms(image).unsqueeze(0)  # Add batch dimension
        return image

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None  # Handle download errors gracefully
    except Exception as e:
        print(f"Error processing image: {e}")
        return None  # Handle other processing errors

# Define classification function (incorporating feedback)
def classify_image(image):
    if image is None:
        return None  # Handle preprocessing errors

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




# API route for image classification
@router.post("/classify")
async def classify(image_url:str = Form(...)):
    image = preprocess_image(image_url)
    if image is None:
        return {"error": "Error processing image."}  # Provide informative error messages

    top_predictions = classify_image(image)
    if top_predictions is None:
        return {"error": "Error performing classification."}

    return {"top_predictions": top_predictions}
