from fastapi import HTTPException
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import tensorflow as tf
import numpy as np
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

def preprocess_image_tflite(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        img = img.resize((180, 180))
        img_array = np.array(img).astype(np.float32)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing image: {str(e)}")

async def classify(request: ClassificationRequest):
    try:
        img_array = preprocess_image_tflite(request.image_url)
    except HTTPException as e:
        raise e

    model_dir = os.path.join("/app", "data")
    normalized_model_path = '/' + request.model_path.strip('/')
    full_model_path = f"{model_dir}{normalized_model_path}"
    full_labels_path = os.path.splitext(full_model_path)[0] + '.json'

    labels = load_labels_from_json(full_labels_path)
        
    if not os.path.isfile(full_model_path):
        raise HTTPException(status_code=404, detail=f"Model file does not exist at {full_model_path}")

    try:
        interpreter = tf.lite.Interpreter(model_path=full_model_path)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()

        output_details = interpreter.get_output_details()
        predictions_lite = interpreter.get_tensor(output_details[0]['index'])
        score_lite = tf.nn.softmax(predictions_lite[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed during the inference process: {str(e)}")

    try:
        top_k_values, top_k_indices = tf.nn.top_k(score_lite, k=5)
        top_predictions = []
        for i in range(5):
            label = labels[top_k_indices.numpy()[i]]
            probability_percent = top_k_values.numpy()[i] * 100
            top_predictions.append({
                "label": label,
                "score": probability_percent
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process prediction results: {str(e)}")

    return {"predictions": top_predictions}