import re
from dataclasses import dataclass
from app.services.chunk_services import ChunkService

@dataclass
class RetrievedChunk:
    chunk_index: int
    content: str
    score: int

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
        self.chunk_service=ChunkService()

    
    
    def tokenize(
        self,
        text: str,
    ) -> set[str]:
        tokens=re.findall(r"\b[a-zA-Z0-9]+\b",text.lower())
        return [ token for token in tokens if token not in STOP_WORDS and len(token)>2]

    def retrieve(
        self,
        paper_content: str,
        question: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        chunks = self.chunk_service.chunk_text(paper_content)
        question_token_list = self.tokenize_list(question)
        question_tokens = set(question_token_list)
        phrase = " ".join(question_token_list)
        retrieved_chunks = []
        for chunk in chunks:
            chunk_tokens = self.tokenize(chunk.content)
            chunk_lower=chunk.content.lower()
            question_lower=question.lower()
            score = len(question_tokens & chunk_tokens)*2
            for token in question_tokens:
                score+=chunk_lower.count(token)
            if phrase and phrase in chunk_lower:
                score += 5
            if score == 0:
                continue
            retrieved_chunks.append(
                RetrievedChunk(
                    chunk_index=chunk.index,
                    content=chunk.content,
                    score=score,
                )
            )

        retrieved_chunks.sort(
            key=lambda chunk: chunk.score,
            reverse=True,
        )

        return retrieved_chunks[:top_k]