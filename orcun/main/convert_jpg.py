from fastapi import FastAPI , HTTPException, File, UploadFile, Form ,Response
from fastapi.responses import JSONResponse
import os
import io 
from PIL import Image
import requests
from io import BytesIO
import time
app = FastAPI()


os.makedirs("orcun/ConvertedImages", exist_ok=True)




@app.post("/classify/")
async def classify(image_url: str = Form(...)):
    response = requests.get(image_url)

    if response.status_code != 200:
        
        raise HTTPException(status_code=422 , detail="Image could not be accessed")
    
    file = Image.open(BytesIO(response.content))   
    try:
        timestamp = int(time.time()) # for different file names
        new_jpg=file.convert('RGB') 
        new_path=f"orcun/convertedImages/{timestamp}.jpg"
        new_jpg.save(new_path,'JPEG')
        
       
        
        return JSONResponse(content = ["cat","tiger","giraffe","puma","lion"])
    
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))
    
    

@app.get("/")
def root():
    return {"message":"Python API convert jpg "}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app , host="0,0,0,0" , port=8000)