from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from app.core.config import get_auth_data
from app.cruds.user import find_one_or_none


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=401,
                            detail="Token not found")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'],
                             algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=401,
                            detail='Token is not valid')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401,
                            detail='User ID not found')

    user = await find_one_or_none(user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=401,
                            detail='User not found')

    return user
