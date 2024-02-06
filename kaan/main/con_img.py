from fastapi import FastAPI, HTTPException
from PIL import Image
import requests
from io import BytesIO
import os
import time
from . import schemas
#import your_ai_model   # (Add the module that contains your AI model here.)

app = FastAPI()

os.makedirs('converted_images', exist_ok=True)


@app.post("/classify/")
async def convert_image(request_data: schemas.ImageURL):

    image_url = request_data.image_url

    try: 

        if not image_url or not image_url.startswith("http"): #This part can be removed from code (optionel or can be add Base64 encoder for google images)
            raise ValueError("Invalid image URL provided.")
        
        response = requests.get(image_url)
        if response.status_code != 200 or 'content-type' not in response.headers or not response.headers['content-type'].startswith('image/'):
            raise HTTPException(status_code=400, detail="Unable to download image or image format not supported.")
        
        if len(response.content) > 10*1024*1024:  #Reject files larger than 10MB(Depends)
            raise HTTPException(status_code=413, detail="Image size too large.")
        
        img = Image.open(BytesIO(response.content))
        image_rgb = img.convert('RGB')
        
        #predicted_results = your_ai_model.predict(image_rgb) # (This will work when the AI model is added)
        predicted_results = ["cat", "tiger", "puma", "lion", "giraffe"]

        timestamp = int(time.time())
        save_path = f"converted_images/{timestamp}_converted.jpg"
        image_rgb.save(save_path, 'JPEG')
        
        public_url = f"/converted_images/{timestamp}_converted.jpg"

        return {
            "message": "Image converted, saved, and analyzed successfully.", #optionel (This is line unnecessary, can be changed )
            "url": public_url, #optionel (This is line unnecessary, can be changed )
            "results": predicted_results # (This will work when the AI model is added)
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    