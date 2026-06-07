from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="cloud.env", extra="ignore")
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_DB: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
@lru_cache
def getSettings() -> Settings:
    # BaseSettings reads env / env_file at runtime; static analysis cannot see those values.
    return Settings()  # pyright: ignore[reportCallIssue]