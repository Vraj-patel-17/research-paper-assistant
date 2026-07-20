from sqlalchemy.orm import Session

from app.services.paper_content_service import PaperContentService
from app.services.retrieval.retrieval_services import RetrievalService
from app.prompts.summary_prompt import build_chat_prompt
from app.services.llm_client import LLMClient
from app.schemas.chat import ChatResponse, SourceReference
from app.services.paper_services import get_paper_by_id
class ChatService:

    def __init__(self, db: Session):
        self.db = db

        self.paper_content_service = PaperContentService()
        self.retrieval_service = RetrievalService()
        self.llm_client = LLMClient()

    def chat(self,paper_id:int,question:str)->ChatResponse:
        paper = get_paper_by_id(self.db,paper_id=paper_id)
        content=self.paper_content_service.get_or_create_content(db=self.db,paper=paper)
        chunks=self.retrieval_service.retrieve(content,question)
        if not chunks:
            return ChatResponse(answer="I couldn't find the answer in the provided paper",sources=[])
        context=self.retrieval_service.build_context(chunks)
        prompt=build_chat_prompt(question=question,context=context)
        answer=self.llm_client.generate_text(prompt=prompt)
        return ChatResponse(answer=answer,sources=[SourceReference(chunk_id=chunk.chunk_id,chunk_index=chunk.chunk_index,) for chunk in chunks],)