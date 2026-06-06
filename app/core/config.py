from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    # App
    APP_NAME: str = "product-service"
    APP_ENV: str = "production"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str  # e.g. postgresql+asyncpg://user:pass@host:5432/db

    # Auth
    SECRET_KEY: str  # openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Rate limiting (requests per minute per IP)
    RATE_LIMIT: str = "60/minute"

    # Observability
    # Leave empty to export traces to stdout (ConsoleSpanExporter).
    # Set to e.g. "https://tempo-prod-xx.grafana.net/otlp" to ship to a collector.
    OTEL_EXPORTER_OTLP_ENDPOINT: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
