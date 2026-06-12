from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./action_engine.sqlite3"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    frontend_origin: str = "http://localhost:3000"
    free_daily_ingest_limit: int = 10

    jwt_secret: str = "change-me-in-production-use-a-real-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
