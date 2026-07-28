from google import genai

from app.core.config import settings

class GeminiClient:
    def __init__(self):
        if not settings.google_api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=settings.google_api_key)