import ssl
import aiohttp
from fastapi import Form, HTTPException, APIRouter
import aiofiles
import os
import certifi

#router = APIRouter(
  #  prefix="/upload_model",  # Prefix for all endpoints within this router
 #   tags=['upload_model']  # Tags for grouping endpoints in the documentation
#)

#@router.post("/")
async def process_file(url: str = Form(...), path: str = Form(...)):
    # Split the path to get the directory and the filename
    target_location, filename = os.path.split(path)
    default_prefix = "/app/data"  # Default directory prefix where files will be saved
    # Validate file extension
    _, file_extension = os.path.splitext(filename)
    if not file_extension in [".pth", ".h5",".tflite"]:
        raise HTTPException(status_code=422, detail="Not allowed file type. Just allowed .pth , .tflite and .h5.")
    
    # Corrected to represent the full path where the file will be saved
    full_path = f"{default_prefix}{target_location}/{filename}"
   
    
    # Create target directory if it doesn't exist
    if not os.path.exists(os.path.dirname(full_path)):
        os.makedirs(os.path.dirname(full_path), exist_ok=True)  # Make directories if they do not exist

    # Use CA certificates path for HTTPS verification
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    try:
        # Using ssl_context for certificate verification
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Error downloading file from URL.")
                
                # Write the content to the file asynchronously
                async with aiofiles.open(full_path, 'wb') as f:
                    await f.write(await response.read())

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=400, detail=f"Error downloading file: {e}")
    except IOError as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

    # Return a success message with the path where the file is saved
    return {"message": f"File processed and saved to {target_location}/{filename}"}