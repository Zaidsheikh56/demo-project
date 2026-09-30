import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://shaadi:shaadi@localhost:5432/shaadi_crm",
    )
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    api_prefix: str = "/api/v1"
    environment: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"


settings = Settings()
