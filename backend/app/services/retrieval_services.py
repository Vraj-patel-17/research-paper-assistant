import re
from dataclasses import dataclass
from app.models.paper_content import PaperContent
from rank_bm25 import BM25Okapi
@dataclass
class RetrievedChunk:
    chunk_index: int
    content: str
    score: float

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
       
    def tokenize(
        self,
        text: str,
    ) -> list[str]:
        tokens=re.findall(r"\b[a-zA-Z0-9]+\b",text.lower())
        return [ token for token in tokens if token not in STOP_WORDS and len(token)>2]

    def retrieve(
        self,
        paper_content: PaperContent,
        question: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        chunks = paper_content.chunks
        if not chunks:
            return []
        tokenized_chunks=[self.tokenize(chunk.text) for chunk in chunks]
        bm25=BM25Okapi(tokenized_chunks)
        question_tokens=self.tokenize(question)
        scores=bm25.get_scores(question_tokens)
        retrieved_chunks = []
        for chunk,score in zip(chunks,scores):
            if score<=0:
                continue
            retrieved_chunks.append(
                RetrievedChunk(
                    chunk_index=chunk.chunk_index,
                    content=chunk.text,
                    score=float(score),
                )
            )

        retrieved_chunks.sort(
            key=lambda chunk: chunk.score,
            reverse=True,
        )

        return retrieved_chunks[:top_k]