from fastapi import APIRouter, Depends, HTTPException
from app.models.users import User
from app.schemas.user import UserUpdateSchema
from app.cruds.user import update_user, delete_user
from app.services.dependencies import get_current_user
from app.services.auth import get_password_hash

router = APIRouter(prefix="/users", tags=['Users'])


@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.put("/me/update")
async def update_profile(
    user_data: UserUpdateSchema,
    current_user: User = Depends(get_current_user)
):
    update_data = {
        k: v
        for k, v in user_data.model_dump().items()
        if v is not None
    }
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update"
        )

    check = await update_user(current_user.user_id,
                              **update_data)
    if check:
        return {"message": "Data updated successfully"}
    else:
        return {"message": "Error updating data"}


@router.delete("/me/delete")
async def delete_self(current_user: User = Depends(get_current_user)):
    check = await delete_user(user_id=current_user.user_id)
    if check:
        return {"message": "User deleted successfully"}
    else:
        return {"message": "Error deleting user"}
