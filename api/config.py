from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_FOLDER: str
    APP_DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str
    DB_HOST: str
    DB_DBNAME: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    TOKEN_SENDING_SERVICE: str

    class Config:
        env_file = Path.cwd() / '.env'


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
