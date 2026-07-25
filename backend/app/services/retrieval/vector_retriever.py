from sqlalchemy.orm import Session

from app.models.paperchunk import PaperChunk
from app.models.paper_content import PaperContent
from app.schemas.retrieval import RetrievedChunk
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.retrieval.base import BaseRetriever
from app.services.retrieval.retrieval_utils import RetrievalUtils
import logging
logger = logging.getLogger(__name__)

class VectorRetriever(BaseRetriever):

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def retrieve(
        self,
        db: Session,
        paper_content: PaperContent,
        question: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:

        question_embedding = self.embedding_service.generate_embedding(question)
        logger.debug("Generated question embedding for vector retrieval")
        distance = PaperChunk.embedding.cosine_distance(question_embedding)
        logger.debug("Performing vector search for paper_content_id=%s",paper_content.id)
        rows = (
            db.query(
                PaperChunk,
                distance.label("distance"),
            )
            .filter(
                PaperChunk.paper_content_id == paper_content.id
            )
            .order_by(distance)
            .limit(top_k)
            .all()
        )

        retrieved_chunks = []

        for chunk, distance in rows:

            if not RetrievalUtils.is_valid_chunk(
                chunk.text,
                chunk.section,
            ):
                continue

            retrieved_chunks.append(
                RetrievedChunk(
                    chunk_id=chunk.id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.text,
                    section=chunk.section,
                    score=1 - float(distance),
                )
            )
        logger.debug("Vector retrieval returned %d chunks",len(retrieved_chunks))
        return retrieved_chunks