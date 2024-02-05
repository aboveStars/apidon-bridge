from pydantic import BaseModel

class ImageURL(BaseModel):
    image_url: str