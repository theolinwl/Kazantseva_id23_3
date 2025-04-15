from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
