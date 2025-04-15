from pydantic import BaseModel


class ImageBinarizationRequest(BaseModel):
    base64_image: str
    algorithm: str
