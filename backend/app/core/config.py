import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    PDF_TIMEOUT: int = int(
        os.getenv("PDF_TIMEOUT", "30")
    )

    SUMMARY_MAX_WORDS: int = int(
        os.getenv("SUMMARY_MAX_WORDS", "300")
    )


settings = Settings()