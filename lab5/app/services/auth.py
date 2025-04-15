from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

from pydantic import EmailStr
from app.core.config import get_auth_data
from app.cruds.user import find_one_or_none

pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(
        to_encode,
        auth_data['secret_key'],
        algorithm=auth_data['algorithm']
    )
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await find_one_or_none(email=email)
    if (
        not user
        or not verify_password(
            plain_password=password,
            hashed_password=user.password
        )
    ):
        return None
    return user
