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
    mdl_url: str
    mdl_path: str

@router.post("/")
async def upload_model(request: ModelUploadRequest):
    directory = os.path.dirname(request.mdl_path)
    if not directory:
        raise HTTPException(status_code=400, detail="Invalid model path provided.")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(request.mdl_url)
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=400, detail=f"Request to {request.mdl_url} failed.") from exc
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Error response {exc.response.status_code} while requesting {request.mdl_url}.") from exc

    os.makedirs(directory, exist_ok=True)
    async with aiofiles.open(request.mdl_path, 'wb') as file:
        await file.write(response.content)
    
    return f"Model successfully downloaded to {request.mdl_path}."