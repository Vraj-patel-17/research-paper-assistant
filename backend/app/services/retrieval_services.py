import re
from dataclasses import dataclass
@dataclass
class RetrievedChunk:
    chunk_index: int
    content: str
    score: int
class RetrievalService:

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(
        self,
        text: str,
    ) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap
        return chunks
    
    def tokenize(self,text: str,) -> set[str]:

        return set(re.findall(r"\w+",text.lower(),))
    
    def retrieve(self,paper_content: str,question: str,top_k: int = 5,) -> list[RetrievedChunk]:
        chunks = self.chunk_text(paper_content)
        question_tokens = self.tokenize(question)
        retrieved_chunks = []

        for index, chunk in enumerate(chunks):
            chunk_tokens = self.tokenize(chunk)
            score = len(question_tokens.intersection(chunk_tokens))
            if score==0:
                continue
            retrieved_chunks.append(RetrievedChunk(chunk_index=index,content=chunk,score=score))

        retrieved_chunks.sort(key=lambda chunk:chunk.score,reverse=True)
        return retrieved_chunks[:top_k]