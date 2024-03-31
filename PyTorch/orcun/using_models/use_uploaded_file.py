from fastapi import Form,HTTPException , APIRouter
from models.tensorflow import host_tfmodel
from models.pytorch import host_ptmodel
from models.tensorflow_lite import host_tflitemodel

router = APIRouter(
    prefix="/test_uploaded_models",
    tags=['test']
)

@router.post("/classify")
async def test_uploaded_models(image_url:str = Form(...),model_path_url:str = Form(...),model_extension : str = Form(...)):
    if model_extension == ".h5":
        return await host_tfmodel.classify(image_url,model_path_url)
    elif model_extension ==".pth":
        return await host_ptmodel.classify(image_url,model_path_url)
    elif model_extension ==".tflite":
        return await host_tflitemodel.classify(image_url,model_path_url)
    else:
        raise HTTPException(status_code=400, detail="Unsupported model ID. Please provide a valid model_id with .h5 or .pth or .tflite extension.")


@router.get("/")
def test():
    return {"Hello world"}