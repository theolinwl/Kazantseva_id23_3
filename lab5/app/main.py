from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.binary_image import router as binary_image_router


app = FastAPI()


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(binary_image_router)
