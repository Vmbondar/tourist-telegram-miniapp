from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Tourist Telegram Mini App"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "tourist_app"

    # Telegram Bot API
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_SECRET_KEY: str

    # Yandex Object Storage (опционально, для будущих этапов)
    YANDEX_STORAGE_ENDPOINT: str = "https://storage.yandexcloud.net"
    YANDEX_STORAGE_BUCKET: Optional[str] = None
    YANDEX_STORAGE_ACCESS_KEY: Optional[str] = None
    YANDEX_STORAGE_SECRET_KEY: Optional[str] = None
    YANDEX_STORAGE_REGION: str = "ru-central1"

    # ЮKassa (опционально, для будущих этапов)
    YOOKASSA_SHOP_ID: Optional[str] = None
    YOOKASSA_SECRET_KEY: Optional[str] = None
    YOOKASSA_TEST_MODE: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
