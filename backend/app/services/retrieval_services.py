import re
from dataclasses import dataclass


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

    def __init__(
        self,
        chunk_size: int = 250,
        chunk_overlap: int = 50,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(
        self,
        text: str,
    ) -> list[str]:
        paragraphs = [
            p.strip()
            for p in re.split(r"\n\s*\n", text)
            if p.strip()
        ]
        chunks = []
        current_words = []

        for paragraph in paragraphs:
            paragraph_words = paragraph.split()
            if len(paragraph_words) > self.chunk_size:

                if current_words:
                    chunks.append(" ".join(current_words))
                    current_words = []

                start = 0

                while start < len(paragraph_words):
                    end = start + self.chunk_size
                    chunks.append(
                        " ".join(paragraph_words[start:end])
                    )
                    start += self.chunk_size - self.chunk_overlap

                continue

            # Paragraph fits
            if len(current_words) + len(paragraph_words) <= self.chunk_size:
                current_words.extend(paragraph_words)
            else:
                chunks.append(" ".join(current_words))
                overlap = current_words[-self.chunk_overlap :] if current_words else []
                current_words = overlap + paragraph_words

        if current_words:
            chunks.append(" ".join(current_words))

        return chunks

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
        chunks = self.chunk_text(paper_content)
        question_token_list = self.tokenize_list(question)
        question_tokens = set(question_token_list)
        phrase = " ".join(question_token_list)
        retrieved_chunks = []
        for index, chunk in enumerate(chunks):
            chunk_tokens = self.tokenize(chunk)
            chunk_lower=chunk.lower()
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
                    chunk_index=index,
                    content=chunk,
                    score=score,
                )
            )

        retrieved_chunks.sort(
            key=lambda chunk: chunk.score,
            reverse=True,
        )

        return retrieved_chunks[:top_k]