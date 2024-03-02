from fastapi import Form, HTTPException,APIRouter
from aiofiles import open as async_open
import requests
import os

router=APIRouter(
    prefix="/upload_model",
    tags=['upload_model']
)

@router.post("/")
async def upload_file(url: str= Form(...),path: str = Form(...)):
    try:
        response = requests.get(url) 
        response.raise_for_status()  
        content = response.content
        
        
        directory, filename = os.path.split(path) # It divides the path input into two parts: the file name and the location where the file will be downloaded.

        
        if not os.path.exists(directory):
            os.makedirs(directory)

        _, file_extension = os.path.splitext(filename)  # It seperate file extension.
        print(file_extension)
        if file_extension not in ['.pth', '.h5']:  # Only .pth and .h5 extensions are allowed.
            raise HTTPException(status_code=400, detail="Unsupported file extension. Only .pth and .h5 are allowed.")
        
        

        file_path = os.path.join(directory, filename)

        
        async with async_open(file_path, 'wb') as file:
            await file.write(content)

        return f"File saved succesfully to this location: {directory}"
    except Exception as e:
        return HTTPException(status_code=400, detail=f"failure: {str(e)}")
