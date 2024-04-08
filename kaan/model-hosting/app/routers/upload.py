from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import aiofiles
import os

router = APIRouter(
    prefix="/upload",
    tags=['Model upload mechanism']
)

class ModelUploadRequest(BaseModel):
    model_url: str
    model_path: str

@router.post("/")
async def upload_model(request: ModelUploadRequest):
    prefixed_path = os.path.join("/app/data", request.model_path)
    directory = os.path.dirname(prefixed_path)

    if not directory:
        raise HTTPException(status_code=400, detail="Invalid model path provided.")

    if os.path.exists(prefixed_path):
        raise HTTPException(status_code=400, detail="Model file already exists.")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(request.model_url)
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=400, detail=f"Request to {request.model_url} failed.") from exc
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Error response {exc.response.status_code} while requesting {request.model_url}.") from exc

    os.makedirs(directory, exist_ok=True)
    
    async with aiofiles.open(prefixed_path, 'wb') as file:
        await file.write(response.content)
    
    return f"Model successfully downloaded to {prefixed_path}."