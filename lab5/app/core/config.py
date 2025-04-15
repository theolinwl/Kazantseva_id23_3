import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "..",
            "..",
            ".env"
        )
    )


settings = Settings()


def get_db_url():
    return (f"sqlite+aiosqlite:///./app/db/{settings.DB_NAME}.db")


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}
