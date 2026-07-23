from app.services.retrieval.bm25_retriever import BM25Retriever
from app.services.retrieval.vector_retriever import VectorRetriever
from app.schemas.retrieval import RetrievedChunk
from app.models.paper_content import PaperContent
from sqlalchemy.orm import Session


class HybridRetriever:

    def __init__(self):
        self.bm25 = BM25Retriever()
        self.vector = VectorRetriever()

    def retrieve(
        self,
        db: Session,
        paper_content: PaperContent,
        question: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:

        bm25_results = self.bm25.retrieve(
            paper_content=paper_content,
            question=question,
            top_k=top_k,
        )
        vector_results = self.vector.retrieve(
            db=db,
            paper_content=paper_content,
            question=question,
            top_k=top_k,
        )
        results=self.merge_results(
            bm25_results,
            vector_results,
            top_k,
        )
        return results

    def merge_results(
    self,
    bm25_results: list[RetrievedChunk],
    vector_results: list[RetrievedChunk],
    top_k: int,
) -> list[RetrievedChunk]:

        merged: dict[int, RetrievedChunk] = {}

        for chunk in bm25_results + vector_results:
            existing = merged.get(chunk.chunk_id)

            if existing is None or chunk.score > existing.score:
                merged[chunk.chunk_id] = chunk

        return sorted(
            merged.values(),
            key=lambda chunk: chunk.score,
            reverse=True,
        )[:top_k]