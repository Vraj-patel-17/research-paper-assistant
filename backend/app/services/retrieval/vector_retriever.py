from sqlalchemy.orm import Session

from app.models.paperchunk import PaperChunk
from app.models.paper_content import PaperContent
from app.schemas.retrieval import RetrievedChunk
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.retrieval.base import BaseRetriever


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

        question_embedding = (self.embedding_service.generate_embedding(question))
        chunks = (
            db.query(PaperChunk)
            .filter(
                PaperChunk.paper_content_id == paper_content.id
            ).order_by(PaperChunk.embedding.cosine_distance(question_embedding))
            .limit(top_k).all())
        return [
            RetrievedChunk(
                chunk_id=chunk.id,
                chunk_index=chunk.chunk_index,
                content=chunk.text,
                section=chunk.section,
                score=0.0,  # improve this later.
            )
            for chunk in chunks
        ]