from abc import ABC, abstractmethod

from app.models.paperchunk import PaperChunk
from app.schemas.retrieval import RetrievedChunk

class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(
        self,
        question: str,
        chunks: list[PaperChunk],
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant chunks for a question.
        """
        pass