import re
from dataclasses import dataclass
from app.models.paper_content import PaperContent
from rank_bm25 import BM25Okapi
from sqlalchemy.orm import Session
from app.models.paperchunk import PaperChunk 
from app.schemas.retrieval import RetrievedChunk,RetrievalDebugResponse,RetrievedChunkResponse
from app.services.retrieval.hybrid_retriver import HybridRetriever
from app.services.paper_content_service import PaperContentService
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at",
    "be", "by", "for", "from",
    "has", "have", "had",
    "in", "into", "is", "it",
    "of", "on", "or", "that",
    "the", "their", "this", "to",
    "was", "were", "will", "with",
    "what", "which", "who", "when",
    "where", "why", "how", "can",
    "could", "should", "would",
}
class RetrievalService:
    def __init__(self):
        self.retriever=HybridRetriever()
    def retrieve(
        self,
        db:Session,
        paper_content: PaperContent,
        question: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        return self.retriever.retrieve(db=db,paper_content=paper_content,question=question,top_k=top_k)
    
    def build_context(self,chunks: list[RetrievedChunk],) -> str:
        context = []
        current_section = None
        for chunk in chunks:
            if chunk.section and chunk.section != current_section:
                context.append(f"## {chunk.section}")
                current_section = chunk.section
            context.append(chunk.content)
        return "\n\n".join(context)

    def retrieve_chunks(
    self,
    db: Session,
    paper_content: PaperContent,
    question: str,
    top_k: int = 5,
) -> list[RetrievedChunk]:

        return self.retriever.retrieve(
            db=db,
            paper_content=paper_content,
            question=question,
            top_k=top_k,
        )

    def search_chunks(
    self,
    paper_id: int,
    question: str,
) -> RetrievalDebugResponse:

        paper = PaperContentService.get_paper_by_id(
            self.db,
            paper_id,
        )

        content = self.paper_content_service.get_or_create_content(
            db=self.db,
            paper=paper,
        )

        chunks = self.retrieval_service.retrieve(
            db=self.db,
            paper_content=content,
            question=question,
        )

        return RetrievalDebugResponse(
            chunks=[
                RetrievedChunkResponse(
                    chunk_id=chunk.chunk_id,
                    chunk_index=chunk.chunk_index,
                    section=chunk.section,
                    score=chunk.score,
                    content=chunk.content,
                )
                for chunk in chunks
            ]
        )