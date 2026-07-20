import re
from dataclasses import dataclass
from app.models.paper_content import PaperContent
from rank_bm25 import BM25Okapi
from app.models.paperchunk import PaperChunk 
from app.schemas.retrieval import RetrievedChunk
from app.services.retrieval.bm25_retriever import BM25Retriever
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
        self.retriever=BM25Retriever()
    def retrieve(
        self,
        paper_content: PaperContent,
        question: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        return self.retriever.retrieve(question=question, paper_content=paper_content, top_k=top_k)
    
    def build_context(self,chunks: list[RetrievedChunk],) -> str:
        context = []
        current_section = None
        for chunk in chunks:
            if chunk.section and chunk.section != current_section:
                context.append(f"## {chunk.section}")
                current_section = chunk.section
            context.append(chunk.content)
        return "\n\n".join(context)
    