from app.services.base_client import GeminiClient
from app.core.config import settings

class EmbeddingService(GeminiClient):
    def __init__(self):
        super().__init__()
        self.model=settings.GEMINI_EMBEDDING_MODEL
    def generate_embedding(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model=self.model,
            contents=text,)

        return response.embeddings[0].values
