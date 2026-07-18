from sqlalchemy.orm import Session

from app.services.paper_content_service import PaperContentService
from app.services.retrieval_services import RetrievalService
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
        print([chunk.chunk_index for chunk in chunks])
        context="\n\n".join(chunk.content for chunk in chunks)
        prompt=build_chat_prompt(question=question,context=context)
        print("----- CONTEXT START -----")
        print(context)
        print("----- CONTEXT END -----")
        answer=self.llm_client.generate_text(prompt=prompt)
        return ChatResponse(answer=answer,sources=[SourceReference(chunk_index=chunk.chunk_index,) for chunk in chunks],)