from fastapi import APIRouter, Depends, HTTPException
from app.models.users import User
from app.services.dependencies import get_current_user
from app.services.binary_image import otsu_binarization, clean_base64
from app.schemas.binary_image import ImageBinarizationRequest
from asyncio import to_thread


router = APIRouter(tags=['Image binarization'])


@router.post("/binary_image")
async def get_binary_image(
    request: ImageBinarizationRequest,
    user: User = Depends(get_current_user)
):
    cleaned = clean_base64(request.base64_image)
    if request.algorithm == 'otsu':
        binarized_image = await to_thread(otsu_binarization, cleaned)
        binarized_image = clean_base64(binarized_image, add_prefix=True)
    else:
        raise HTTPException(status_code=400, detail="Algorythm not supported")
    return {"binarized_image": binarized_image}
