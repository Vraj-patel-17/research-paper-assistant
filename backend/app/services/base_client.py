from functools import lru_cache

from google import genai

from app.core.config import settings


class GeminiClient:
    """Base class for services that call the Gemini API.

    Subclasses share one underlying genai.Client instead of each opening
    their own (EmbeddingService and LLMClient previously each created a
    separate client for no reason).
    """

    def __init__(self):
        self.client = _get_shared_client()


@lru_cache(maxsize=1)
def _get_shared_client() -> genai.Client:
    if not settings.google_api_key:
        raise ValueError("GEMINI_API_KEY is not set.")
    return genai.Client(api_key=settings.google_api_key)