from fastapi import APIRouter, HTTPException, Response

from app.schemas.user import UserSchema
from app.cruds.user import create_user, find_one_or_none
from app.services.auth import (get_password_hash,
                               authenticate_user,
                               create_access_token)

router = APIRouter(tags=['Auth'])


@router.post("/sign-ip/")
async def sign_up(user_data: UserSchema, response: Response):
    user = await find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(status_code=409,
                            detail="User already exists")
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    check = await create_user(**user_dict)

    access_token = create_access_token({"sub": str(check.user_id)})
    response.set_cookie(
        key="users_access_token",
        value=access_token,
        httponly=True
    )

    if check:
        return {
            "id": check.user_id,
            "email": check.email,
            "token": access_token
        }
    else:
        return {"message": "Error during sign-up"}


@router.post("/login/")
async def login(user_data: UserSchema, response: Response):
    check = await authenticate_user(
        email=user_data.email,
        password=user_data.password
    )
    if check is None:
        raise HTTPException(status_code=401,
                            detail="Wrong email or password")
    access_token = create_access_token({"sub": str(check.user_id)})
    response.set_cookie(
        key="users_access_token",
        value=access_token,
        httponly=True
    )
    return {"id": check.user_id, "email": check.email, "token": access_token}
