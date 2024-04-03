from fastapi import FastAPI, Form, HTTPException, APIRouter
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
import requests

router = APIRouter(
    prefix="/tensorflow_lite",
    tags=['tensorflow_lite']
)

# Parameters for image processing
img_height = 180
img_width = 180

# List of character names for classification results
class_names = ['abraham_grampa_simpson', 'agnes_skinner', 'apu_nahasapeemapetilon', 
               'barney_gumble', 'bart_simpson', 'carl_carlson', 'charles_montgomery_burns', 
               'chief_wiggum', 'cletus_spuckler', 'comic_book_guy', 'edna_krabappel', 
               'groundskeeper_willie', 'homer_simpson', 'kent_brockman', 'krusty_the_clown', 
               'lenny_leonard', 'lisa_simpson', 'maggie_simpson', 'marge_simpson', 'martin_prince', 
               'mayor_quimby', 'milhouse_van_houten', 'moe_szyslak', 'ned_flanders', 'nelson_muntz', 
               'patty_bouvier', 'principal_skinner', 'professor_john_frink', 'rainier_wolfcastle', 
               'ralph_wiggum', 'selma_bouvier', 'sideshow_bob', 'sideshow_mel', 'snake_jailbird', 
               'waylon_smithers'] 


async def classify(image_url: str = Form(...),model_path_url:str = Form(...)):
    try:
        # Preprocess the image
        img_array = preprocess_image_tflite(image_url)
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
        top_k_values, top_k_indices = tf.nn.top_k(score_lite, k=5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during model prediction: {e}")

    results = [{"class": class_names[i], "probability": f"{prob:.2f}%"} for i, prob in zip(top_k_indices.numpy(), top_k_values.numpy() * 100)]

    return {"predictions": results}

def preprocess_image_tflite(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB").resize((img_height, img_width))
        img_array = np.array(img).astype(np.float32)
        img_array = np.expand_dims(img_array, axis=0)  # Create a batch
        return img_array
    else:
        return None