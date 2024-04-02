from fastapi import Form, APIRouter
from PIL import Image
from io import BytesIO
import requests
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn as nn

router = APIRouter(
    prefix="/pytorch",
    tags=['pytorch']
)

#model_yeri = 'models/pytorch/model_23.pth'

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

@router.get("/")
def root():
    return {"message": "This is the PyTorch model."}


async def classify(image_url: str = Form(...),model_path_url:str = Form(...)):
    # Model loading and initialization
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 10)  # Sabit 10 sınıf

    try:
        state_dict = torch.load(f"/app/data{model_path_url}")
        model.load_state_dict(state_dict)
    except FileNotFoundError:
        return {"error": "Model state dictionary not found."}

    model.eval()

    # Image preprocessing
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
    except requests.exceptions.RequestException as e:
        return {"error": f"Error downloading image: {e}"}
    except Exception as e:
        return {"error": f"Error processing image: {e}"}

    # Image classification
    try:
        output = model(image)
        probs, indices = torch.topk(output, 5)
        probs = torch.nn.functional.softmax(probs, dim=1)

        top_predictions = []
        for i in range(5):
            top_predictions.append({
                "class_name": classes[indices[0][i].item()],
                "probability": probs[0][i].item() * 100
            })

        return {"top_predictions": top_predictions}
    except Exception as e:
        return {"error": f"Error performing classification: {e}"}