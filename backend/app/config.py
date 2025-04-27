from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import json


class Settings(BaseSettings):
    # Настройки приложения
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Настройки ВКонтакте
    VK_CLIENT_ID: str
    VK_CLIENT_SECRET: str
    VK_REDIRECT_URI: str
    FRONTEND_URL: str

    # База данных
    DATABASE_URL: str

    # CORS
    CORS_ORIGINS: List[str]

    class Config:
        env_file = ".env"

    def __init__(self, **data):
        super().__init__(**data)
        # Парсинг строковых списков из переменных окружения
        if isinstance(self.CORS_ORIGINS, str):
            self.CORS_ORIGINS = json.loads(self.CORS_ORIGINS)


@lru_cache()
def get_settings():
    return Settings()