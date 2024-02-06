from pydantic import BaseModel

class ImageURL(BaseModel): # Defining Image_url schemas
    image_url: str