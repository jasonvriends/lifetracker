from typing import Any

from pydantic import BaseSettings, EmailStr, MongoDsn

from config.constants import Environment


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str
    APP_VERSION: str

    # MongoDB settings
    DATABASE_URI: MongoDsn

    # Environment settings
    ENVIRONMENT: Environment = Environment.PRODUCTION

    # CORS settings
    CLIENT_ORIGIN: str

    # Fief settings
    CLIENT_ID: str
    CLIENT_SECRET: str
    FIEF_URL: str
    AUTHORIZE_URL: str
    TOKEN_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        orm_mode = True
        case_sensitive = True


settings = Settings()

# FastAPI app config
app_configs: dict[str, Any] = {
    "title": settings.APP_NAME,
    "version": settings.APP_VERSION,
}

## Remove docs and redocs in Production
if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None
    app_configs["redocs_url"] = None
