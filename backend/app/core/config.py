from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    app_name: str = "Research Paper Assistant"
    debug: bool = False

    # Database
    database_url: str

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Gemini
    google_api_key: str

    # RAG
    embedding_model: str = "gemini-embedding-001"
    llm_model: str = "gemini-2.5-flash"

    # Chunking
    chunk_size: int = Field(default=250, gt=0)
    chunk_overlap: int = Field(default=50, ge=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    allowed_origins: list[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )#later replace with frontend url


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()