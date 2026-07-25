from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.summary import Summary

from app.services.paper_content_service import paper_content_service
from app.services.llm_client import LLMClient
from app.prompts.summary_prompt import build_summary_prompt
import logging
logger = logging.getLogger(__name__)
class SummaryService:

    def get_by_paper_id(
        self,
        db: Session,
        paper_id: int,
        summary_type: str = "standard",
    ) -> Summary | None:
        return (
            db.query(Summary)
            .filter(
                Summary.paper_id == paper_id,
                Summary.summary_type == summary_type,
            )
            .first()
        )

    def create(
        self,
        db: Session,
        paper_id: int,
        summary_type: str,
        model_name: str,
        content: str,
    ) -> Summary:

        summary = Summary(
            paper_id=paper_id,
            summary_type=summary_type,
            model_name=model_name,
            content=content,
        )

        db.add(summary)
        db.commit()
        db.refresh(summary)

        return summary

    def update(
        self,
        db: Session,
        summary: Summary,
        content: str,
        model_name: str,
    ) -> Summary:

        summary.content = content
        summary.model_name = model_name

        db.commit()
        db.refresh(summary)

        return summary

    def delete(
        self,
        db: Session,
        summary: Summary,
    ) -> None:

        db.delete(summary)
        db.commit()
    def get_or_create_summary(
        self,
        db: Session,
        paper: Paper,
        summary_type: str = "standard",
    ) -> Summary:

        summary = self.get_by_paper_id(
            db=db,
            paper_id=paper.id,
            summary_type=summary_type,
        )

        if summary:
            logger.debug("Using cached summary for paper %s", paper.id)
            return summary

        content = paper_content_service.get_or_create_content(
            db=db,
            paper=paper,
        )
        logger.info("Preparing content for summary generation for paper %s",paper.id,)
        llm = LLMClient()

        prompt = build_summary_prompt(title=paper.title,full_text=content)
        logger.info("Generating summary for paper %s", paper.id)
        generated_summary = llm.generate_text(prompt)

        summary=self.create(
            db=db,
            paper_id=paper.id,
            summary_type=summary_type,
            model_name=llm.model,
            content=generated_summary,
        )
        logger.info("Summary created for paper %s",paper.id,)
        return summary

summary_service = SummaryService()