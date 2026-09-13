from app.services.base_client import GeminiClient
from app.core.config import settings
from google.genai import types
import logging

logger = logging.getLogger(__name__)


class EmbeddingService(GeminiClient):
    def __init__(self):
        super().__init__()
        self.model = settings.embedding_model

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        try:
            logger.info("Generating embeddings for %d texts", len(texts))

            response = self.client.models.embed_content(
                model=self.model,
                contents=texts,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
            )

            embeddings = [embedding.values for embedding in response.embeddings]

            if len(embeddings) != len(texts):
                raise RuntimeError(
                    "Embedding response count does not match input count."
                )

            logger.debug("Generated %d embeddings", len(embeddings))
            return embeddings

        except Exception:
            logger.exception("Failed to generate embeddings")
            raise

    def generate_chunk_embeddings(self, chunks: list[str]) -> list[list[float]]:
        return self.generate_embeddings(chunks)

    def generate_query_embedding(self, query: str) -> list[float]:
        if not query.strip():
            raise ValueError("Query must not be empty.")

        try:
            response = self.client.models.embed_content(
                model=self.model,
                contents=query,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
            )
            return response.embeddings[0].values

        except Exception:
            logger.exception("Failed to generate query embedding")
            raise