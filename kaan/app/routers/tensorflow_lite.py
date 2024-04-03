from fastapi import HTTPException
from pydantic import BaseModel
from keras.models import load_model
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
import requests
import os

class ClassificationRequest(BaseModel):
    image_url: str
    model_path_url: str

img_height = 180
img_width = 180

class_names = [
    'abraham_grampa_simpson', 'agnes_skinner', 'apu_nahasapeemapetilon', 
    'barney_gumble', 'bart_simpson', 'carl_carlson', 'charles_montgomery_burns', 
    'chief_wiggum', 'cletus_spuckler', 'comic_book_guy', 'edna_krabappel', 
    'groundskeeper_willie', 'homer_simpson', 'kent_brockman', 'krusty_the_clown', 
    'lenny_leonard', 'lisa_simpson', 'maggie_simpson', 'marge_simpson', 'martin_prince', 
    'mayor_quimby', 'milhouse_van_houten', 'moe_szyslak', 'ned_flanders', 'nelson_muntz', 
    'patty_bouvier', 'principal_skinner', 'professor_john_frink', 'rainier_wolfcastle', 
    'ralph_wiggum', 'selma_bouvier', 'sideshow_bob', 'sideshow_mel', 'snake_jailbird', 
    'waylon_smithers'
]

def preprocess_image_tflite(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        raise HTTPException(status_code=400, detail=f"HTTP error occurred while retrieving image: {http_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving image: {str(e)}")

    try:
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        img = img.resize((img_height, img_width))
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
    model_path = os.path.join(model_dir, request.model_path_url)
        
    if not os.path.isfile(model_path):
        raise HTTPException(status_code=404, detail=f"Model file does not exist at {model_path}")

    try:
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load TensorFlow Lite model: {str(e)}")

    try:
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
            predicted_class_name = class_names[top_k_indices.numpy()[i]]
            probability_percent = top_k_values.numpy()[i] * 100
            top_predictions.append({
                "class_name": predicted_class_name,
                "probability": probability_percent
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process prediction results: {str(e)}")

    return {"top_predictions": top_predictions}