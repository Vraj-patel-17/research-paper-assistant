from dataclasses import dataclass

@dataclass
class RetrievedChunk:
    chunk_id: int
    chunk_index: int
    content: str
    section: str | None
    score: float