from fastapi import HTTPException , Form,APIRouter
from keras.models import load_model
import tensorflow as tf
from PIL import Image
from io import BytesIO
import requests
import json
import os
import aiofiles
import aiohttp





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
    

async def preprocess_image(url,img_height,img_width):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code = 422,detail = f"Error downloading image: {response.reason}")
                
                image_data = await response.read()
        
        response.raise_for_status()
        image = Image.open(BytesIO(image_data)).convert('RGB')
        image = image.resize((img_height, img_width))
        img_array = tf.keras.utils.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)
        return img_array
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=422, detail=f"Error downloading image: {e}")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error processing image: {e}")




async def classify(image_url: str = Form(...),model_path_url:str = Form(...),img_height:str = Form(...),img_width:str = Form(...)):
    img_height = int(img_height)
    img_width = int(img_width)
    try:
        full_model_path = "/app/data" + model_path_url 
        full_labels_path = os.path.split(full_model_path)[0] + '/label.json'
        class_names ,num_classes = await load_labels_from_json(full_labels_path)
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=f"class names should be under the 'labels' key: {ve}")
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Error reading labels: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while loading class names from JSON: {str(e)}")

    
    try:
        img_array = await preprocess_image(image_url,img_height,img_width)
        model = load_model(f"/app/data{model_path_url}")
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model loading failed: {e}")

    model_num_classes = model.output_shape[-1]
    
    if model_num_classes != num_classes:
        raise HTTPException(status_code = 422, detail =f"Warning: The number of classes in the model ({model_num_classes}) does not match the input number of classes ({num_classes}).")


    try:
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        top_k_values, top_k_indices = tf.nn.top_k(score, k=5)

        response_data = {"predictions": []}
        for i in range(5):
            class_name = class_names[top_k_indices.numpy()[i]]
            probability = top_k_values.numpy()[i]*100
            response_data["predictions"].append(
                {"class_name": class_name, "probability": f"{probability:.2f}%"}
            )
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction: {e}")


    

        
        