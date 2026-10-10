import asyncio
import logging

from google.genai import types

from app.core.config import settings
from app.services.base_client import GeminiClient

logger = logging.getLogger(__name__)


class EmbeddingService(GeminiClient):
    BATCH_SIZE = 100
    BATCH_DELAY_SECONDS = 15  # stay under free-tier ~100 req/min

    def __init__(self):
        super().__init__()
        self.model = settings.embedding_model
        self.dimensions = settings.embedding_dimensions

    def _config(self, task_type: str) -> types.EmbedContentConfig:
        return types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=self.dimensions,
        )

    def _embed_batch_sync(self, texts: list[str]) -> list[list[float]]:
        response = self.client.models.embed_content(
            model=self.model,
            contents=texts,
            config=self._config("RETRIEVAL_DOCUMENT"),
        )
        embeddings = [embedding.values for embedding in response.embeddings]

        if len(embeddings) != len(texts):
            raise RuntimeError(
                "Embedding response count does not match input count."
            )

        return embeddings

    async def generate_chunk_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        all_embeddings: list[list[float]] = []

        try:
            logger.info("Generating embeddings for %d texts", len(texts))

            for i in range(0, len(texts), self.BATCH_SIZE):
                batch = texts[i : i + self.BATCH_SIZE]
                batch_embeddings = await asyncio.to_thread(self._embed_batch_sync, batch)
                all_embeddings.extend(batch_embeddings)

                if i + self.BATCH_SIZE < len(texts):
                    await asyncio.sleep(self.BATCH_DELAY_SECONDS)

            logger.debug("Generated %d embeddings", len(all_embeddings))
            return all_embeddings

        except Exception:
            logger.exception("Failed to generate embeddings")
            raise

    def _generate_query_embedding_sync(self, query: str) -> list[float]:
        if not query.strip():
            raise ValueError("Query must not be empty.")

        try:
            response = self.client.models.embed_content(
                model=self.model,
                contents=query,
                config=self._config("RETRIEVAL_QUERY"),
            )
            return response.embeddings[0].values

        except Exception:
            logger.exception("Failed to generate query embedding")
            raise

    async def generate_query_embedding(self, query: str) -> list[float]:
        return await asyncio.to_thread(self._generate_query_embedding_sync, query)