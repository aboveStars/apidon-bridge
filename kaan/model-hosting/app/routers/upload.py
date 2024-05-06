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
    model_filename = os.path.basename(request.model_path)
    label_filename = os.path.splitext(model_filename)[0] + ".json"

    prefixed_model_path = os.path.join("/app/data", request.model_path)
    prefixed_label_path = os.path.join(os.path.dirname(prefixed_model_path), label_filename)
    
    directory = os.path.dirname(prefixed_model_path)

    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    if os.path.exists(prefixed_model_path) or os.path.exists(prefixed_label_path):
        raise HTTPException(status_code=400, detail="Model or label file already exists.")

    async with httpx.AsyncClient() as client:
        try:
            response_model = await client.get(request.model_url)
            response_label = await client.get(request.label_url)
            response_model.raise_for_status()
            response_label.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=400, detail=f"Request failed: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Error response {exc.response.status_code} while requesting.") from exc

    async with aiofiles.open(prefixed_model_path, 'wb') as model_file:
        await model_file.write(response_model.content)

    async with aiofiles.open(prefixed_label_path, 'w') as label_file:
        label_data = response_label.json()
        await label_file.write(json.dumps(label_data))
    
    return f"Model and label successfully downloaded to {prefixed_model_path} and {prefixed_label_path}."
