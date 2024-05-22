from fastapi import  Form, HTTPException
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
import requests
import json
import os
import aiofiles
import aiohttp

# Parameters for image processing
img_height = 180
img_width = 180

# List of character names for classification results

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



async def classify(image_url: str = Form(...),model_path_url:str = Form(...)):

    try:
        full_model_path = "/app/data" + model_path_url 
        full_labels_path = os.path.split(full_model_path)[0] + '/label.json'
        labels , num_classes = await load_labels_from_json(full_labels_path)
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=f"class names should be under the 'labels' key: {ve}")
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Error reading labels: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while loading class names from JSON: {str(e)}")

    try:
        # Preprocess the image
        img_array = await preprocess_image_tflite(image_url)
        if img_array is None:
            raise HTTPException(status_code=400, detail="Image could not be processed.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"An error occurred while fetching the image from the URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unknown error occurred during image processing: {e}")

    try:
        # Load and use the TensorFlow Lite model
        interpreter = tf.lite.Interpreter(f"/app/data{model_path_url}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while loading the model: {e}")

    try:
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        output_details = interpreter.get_output_details()
        predictions_lite = interpreter.get_tensor(output_details[0]['index'])
        
        score_lite = tf.nn.softmax(predictions_lite[0])
        top_k_values, top_k_indices = tf.nn.top_k(score_lite, k=num_classes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during model prediction: {e}")

    results = [{"class": labels[i], "probability": f"{prob:.2f}%"} for i, prob in zip(top_k_indices.numpy(), top_k_values.numpy() * 100)]

    return {"predictions": results}

async def preprocess_image_tflite(image_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    raise HTTPException(status_code = 422, detail = f"Error downloading image: {response.reason}")
    
                image_data = await response.read()

    
            img = Image.open(BytesIO(image_data))
            img = img.convert("RGB").resize((img_height, img_width))
            img_array = np.array(img).astype(np.float32)
            img_array = np.expand_dims(img_array, axis=0)  # Create a batch
            return img_array
    except Exception as e:
        raise HTTPException(status_code=422, detail= f"preprocess failed : {str(e)}")