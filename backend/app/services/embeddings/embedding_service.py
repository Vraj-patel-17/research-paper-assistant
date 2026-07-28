from app.services.base_client import GeminiClient
from app.core.config import settings
import logging
logger = logging.getLogger(__name__)
class EmbeddingService(GeminiClient):
    def __init__(self):
        super().__init__()
        self.model=settings.embedding_model
    def generate_embedding(self, text: str) -> list[float]:
        try:
            logger.info("Generating embeddings") 
            response = self.client.models.embed_content(
                model=self.model,
                contents=text,)
            logger.debug("Embedding generated successfully")
            return response.embeddings[0].values
        except Exception:
            logger.exception("Failed to generate embedding")
            raise
