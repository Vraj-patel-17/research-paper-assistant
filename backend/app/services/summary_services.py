from sqlalchemy.orm import Session

from app.models.summary import Summary
from app.schemas.summary import SummaryCreate
from app.services.llm_client import LLMClient
from app.models.paper import Paper
from app.schemas.summary import SummaryCreate
from app.prompts.summary_prompt import build_summary_prompt
from app.services.paper_content_service import PaperContentService
class SummaryService:
    def __init__(self, db: Session):
        self.db = db
        self.llm=LLMClient()

    def get_by_paper_id(self, paper_id: int) -> Summary | None:
        return (
            self.db.query(Summary)
            .filter(Summary.paper_id == paper_id)
            .first()
        )

    def create(
        self,
        paper_id: int,
        summary: SummaryCreate,
        model_name: str | None = None,
    ) -> Summary:
        db_summary = Summary(
            paper_id=paper_id,
            summary_text=summary.summary_text,
            model_name=model_name,
        )

        self.db.add(db_summary)
        self.db.commit()
        self.db.refresh(db_summary)

        return db_summary

    def update(
        self,
        db_summary: Summary,
        summary_text: str,
        model_name: str | None = None,
    ) -> Summary:
        db_summary.summary_text = summary_text
        db_summary.model_name = model_name

        self.db.commit()
        self.db.refresh(db_summary)

        return db_summary

    def delete(self, db_summary: Summary):
        self.db.delete(db_summary)
        self.db.commit()
    
    def generate_summary(self, paper_id: int) -> Summary:
    
        paper = (
            self.db.query(Paper)
            .filter(Paper.id == paper_id)
            .first()
        )

        if paper is None:
            raise ValueError("Paper not found.")
        content_service = PaperContentService(self.db)
        paper_content = content_service.get_or_extract(paper_id)
        # Return cached summary if it already exists
        existing_summary = self.get_by_paper_id(paper_id)
        if existing_summary:
            return existing_summary

        prompt =build_summary_prompt(title=paper.title,full_text=paper_content.full_text)
        summary_text = self.llm.generate(prompt)
        summary = SummaryCreate(summary_text=summary_text)
        return self.create(
            paper_id=paper_id,
            summary=summary,
            model_name=self.llm.model,
        )