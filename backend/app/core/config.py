from functools import lru_cache
import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
ENV_FILE=os.getenv("ENV_FILE",".env")
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
    google_api_key: str = Field(alias="GEMINI_API_KEY")

    # RAG
    embedding_model: str = "gemini-embedding-001"
    # pgvector's HNSW index supports at most 2000 dims for `vector`
    embedding_dimensions: int = Field(default=768, gt=0, le=2000)
    llm_model: str = "gemini-2.5-flash"

    # Chunking
    chunk_size: int = Field(default=250, gt=0)
    chunk_overlap: int = Field(default=50, ge=0)

    # ge=3.0: arXiv allows at most one request every 3 seconds
    arxiv_min_interval_seconds: float = Field(default=3.0, ge=3.0)
    arxiv_user_agent: str = "ResearchPaperAssistant/1.0"
    # How long extracted paper text + chunk embeddings may stay cached
    chunk_cache_ttl_days: int = Field(default=7, ge=1)

    PDF_TIMEOUT : int = 30
    SUMMARY_MAX_WORDS: int=200
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )
    allowed_origins: list[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173"
        ]
    )#later replace with frontend url


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()