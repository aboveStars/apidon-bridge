from fastapi import FastAPI, HTTPException,Form
from fastapi.middleware.cors import CORSMiddleware
from keras.models import load_model
import tensorflow as tf
from PIL import Image
from io import BytesIO
import requests


app = FastAPI()


origins = [""]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)





img_height = 128
img_width = 128
class_names = ['Apple', 'Banana', 'Grape', 'Mango', 'Strawberry']


def preprocess_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert('RGB')
        image = image.resize((img_height, img_width))
        img_array = tf.keras.utils.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)
        return img_array
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image from URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")


@app.get("/")
async def root():
    return {"message": "Hello from the image classification API"}


@app.post("/classify")
async def classify(image_url:str =Form(...)):
    try:
        img_array = preprocess_image(image_url)
        model_path = "main/arch12.h5"
        model = load_model(model_path)
    except HTTPException as e:

        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model loading failed: {e}")

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