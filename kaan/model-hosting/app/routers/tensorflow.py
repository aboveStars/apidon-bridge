from fastapi import  HTTPException
from pydantic import BaseModel
from keras.models import load_model
from PIL import Image
from io import BytesIO
import tensorflow as tf
import requests
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

def preprocess_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert('RGB')
        image = image.resize((128, 128))
        img_array = tf.keras.utils.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)
        return img_array
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image from URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")

async def classify(request: ClassificationRequest):
    try:
        img_array = preprocess_image(request.image_url)
        normalized_model_path = '/' + request.model_path_url.strip('/')
        full_model_path = f"/app/data{normalized_model_path}"
        full_labels_path = os.path.splitext(full_model_path)[0] + '.json'

        labels = load_labels_from_json(full_labels_path)
        
        model = load_model(full_model_path)
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        top_k_values, top_k_indices = tf.nn.top_k(score, k=5)

        response_data = {"predictions": []}
        for i in range(5):
            label = labels[top_k_indices.numpy()[i]]
            probability = top_k_values.numpy()[i] * 100
            response_data["predictions"].append({
                  "label": label,
                  "score": f"{probability:.2f}%"
            })

        return response_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction: {e}")