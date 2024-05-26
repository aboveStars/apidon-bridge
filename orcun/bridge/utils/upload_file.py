import ssl
import aiohttp
from fastapi import Form, HTTPException
import os
import certifi
import aiofiles
import logging
import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def process_file(url: str = Form(...), path: str = Form(...), label_url: str = Form(...)):
    logger.debug("Processing file with URL: %s, path: %s, label_url: %s", url, path, label_url)

    # Split the path to get the directory and the filename
    target_location, filename = os.path.split(path)
    default_prefix = "/app/data"  # Default directory prefix where files will be saved
    
    # Validate file extension
    _, file_extension = os.path.splitext(filename)
    if not file_extension in [".pth", ".h5", ".tflite"]:
        raise HTTPException(status_code=422, detail="Not allowed file type. Just allowed .pth, .tflite, and .h5.")
    
    # Corrected to represent the full path where the file will be saved
    full_path = f"{default_prefix}{target_location}/{filename}"
    
    # Split the label URL path to get the directory and the filename
    label_filename = "label"

    
    # Validate label file extension
    temp_file_extension = label_url.split('.')[-1]
    label_file_extension = temp_file_extension.split('?')[0]
    
    if not label_file_extension == "json":
        raise HTTPException(status_code=422, detail="Not allowed label file type. Just allowed .json.")


    
    # Corrected to represent the full path where the label file will be saved
    label_full_path = f"{default_prefix}{target_location}/{label_filename}.{label_file_extension}"
    
    # Create target directories if they don't exist
    for directory in [os.path.dirname(full_path), os.path.dirname(label_full_path)]:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)  # Make directories if they do not exist
    
    # Use CA certificates path for HTTPS verification
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    try:
        # Download and save the main file
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Error downloading file from URL.")
                
                # Write the content to the file asynchronously
                async with aiofiles.open(full_path, 'wb') as f:
                    await f.write(await response.read())
                    logger.debug("Downloaded and saved file to: %s", full_path)


        # Download and save the label file
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(label_url) as label_response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Error downloading label file from URL.")
                
                # Write the content to the label file asynchronously
                async with aiofiles.open(label_full_path, 'wb') as f:
                    await f.write(await label_response.read())
                    logger.debug("Downloaded and saved label file to: %s", label_full_path)

    except aiohttp.ClientError as e:
        logger.error("Error downloading file: %s", e)
        raise HTTPException(status_code=400, detail=f"Error downloading file: {e}")
    except IOError as e:
        logger.error("Error saving file: %s", e)
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

    # Return a success message with the paths where the files are saved
    logger.debug("Files processed and saved to %s and %s", full_path, label_full_path)
    return {"message": f"Files processed and saved to {target_location}/{filename} and {target_location}/label.json"}
