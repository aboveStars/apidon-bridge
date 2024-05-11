from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import aiofiles
import os
import json

router = APIRouter(
    prefix="/upload",
    tags=['Model upload mechanism']
)

class ModelUploadRequest(BaseModel):
    model_url: str
    model_path: str
    label_url: str

@router.post("/")
async def upload_model(request: ModelUploadRequest):
    normalized_model_path = '/' + request.model_path.strip('/')

    model_filename = os.path.basename(normalized_model_path)
    label_filename = os.path.splitext(model_filename)[0] + ".json"

    prefixed_model_path = f'/app/data{normalized_model_path}'
    prefixed_label_path = os.path.join(os.path.dirname(prefixed_model_path), label_filename)
    
    directory = os.path.dirname(prefixed_model_path)
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    existing_model_content = None
    existing_label_content = None
    if os.path.exists(prefixed_model_path):
        async with aiofiles.open(prefixed_model_path, 'rb') as file:
            existing_model_content = await file.read()
    if os.path.exists(prefixed_label_path):
        async with aiofiles.open(prefixed_label_path, 'r') as file:
            existing_label_content = await file.read()

    try:
        async with httpx.AsyncClient() as client:
            response_model = await client.get(request.model_url)
            response_label = await client.get(request.label_url)
            response_model.raise_for_status()
            response_label.raise_for_status()

        model_changed = existing_model_content != response_model.content
        label_changed = existing_label_content != json.dumps(response_label.json())

        async with aiofiles.open(prefixed_model_path, 'wb') as model_file:
            await model_file.write(response_model.content)

        async with aiofiles.open(prefixed_label_path, 'w') as label_file:
            label_data = response_label.json()
            await label_file.write(json.dumps(label_data))

        if not existing_model_content and not existing_label_content:
            return f"Model and label successfully downloaded to {prefixed_model_path} and {prefixed_label_path}."
        elif model_changed or label_changed:
            message_parts = []
            if model_changed:
                message_parts.append(f"Model file at {prefixed_model_path} has been updated.")
            if label_changed:
                message_parts.append(f"Label file at {prefixed_label_path} has been updated.")
            return " ".join(message_parts)
        else:
            return f"No changes were made to the files at {prefixed_model_path} and {prefixed_label_path}."

    except (httpx.RequestError, httpx.HTTPStatusError) as http_exc:
        return f"HTTP error occurred: {http_exc}"
    except (IOError, OSError) as io_exc:
        return f"File writing error: {io_exc}"
    except (ValueError, json.JSONDecodeError) as json_exc:
        return f"JSON processing error: {json_exc}"
