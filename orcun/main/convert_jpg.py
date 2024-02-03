from fastapi import FastAPI , HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
import os
import io
from PIL import Image

app = FastAPI()

DIRECTORY= "/Users/mustafaorcunucgun/Documents/apidon/apidon_bridge/converted_images"
os.makedirs(DIRECTORY, exist_ok=True)

@app.post("/convert_jpg/")
async def convert_jpg(file: UploadFile = File(...)):
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content))

        new_image_path = os.path.join(DIRECTORY , f"{file.filename.rsplit('.',1)[0]}.jpg")
        image.convert('RGB').save(new_image_path , 'JPEG')

        return JSONResponse(content = ["cat","tiger","giraffe","puma","lion"])
    
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))
    

@app.get("/")
def root():
    return {"message":"Python API convert jpg "}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app , host="0,0,0,0" , port=8000)