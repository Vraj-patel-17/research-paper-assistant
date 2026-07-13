from sqlalchemy.orm import Session

from app.services.paper_content_service import PaperContentService
from app.services.retrieval_services import RetrievalService
from app.prompts.summary_prompt import build_chat_prompt
from app.services.llm_client import LLMClient
from app.schemas.chat import ChatResponse, SourceReference
class ChatService:

    def __init__(self, db: Session):
        self.db = db

        self.paper_content_service = PaperContentService()
        self.retrieval_service = RetrievalService()
        self.llm_client = LLMClient()

    def chat(self,paper_id:int,question:str)->ChatResponse:
        paper_content = self.paper_content_service.get_by_paper_id(self.db,paper_id)
        chunks=self.retrieval_service.retrieve(paper_content.content,question)
        context="\n\n".join(chunk.content for chunk in chunks)
        prompt=build_chat_prompt(question=question,context=context)
        answer=self.llm_client.generate_text(prompt=prompt)
        return ChatResponse(answer=answer,sources=[SourceReference(chunk_index=chunk.chunk_index,) for chunk in chunks],)