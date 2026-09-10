from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.services.paper_services import get_paper_by_id
from app.services.pdf_service import pdf_service
from app.services.llm_client import LLMClient
from app.prompts.summary_prompt import build_summary_prompt
from app.models.paper_summary import PaperSummary

def generate_paper_summary(
    db: Session,
    paper_id: UUID,
) -> str:

    paper = get_paper_by_id(db, paper_id)

    if not paper:
        raise LookupError("Paper not found")
    if not paper.pdf_url:
        raise ValueError("Paper does not have a PDF URL")
    existing_summary = db.execute(
    select(PaperSummary).where(
        PaperSummary.paper_id == paper_id
    )   ).scalar_one_or_none()

    if existing_summary:
        return existing_summary.summary

    full_text = pdf_service.extract_from_url(paper.pdf_url)

    prompt = build_summary_prompt(
        title=paper.title,
        full_text=full_text,
    )

    llm_client = LLMClient()
    summary_text = llm_client.generate_text(prompt)
    paper_summary=PaperSummary(
        paper_id=paper_id,
        summary=summary_text
    )
    db.add(paper_summary)
    db.commit()
    db.refresh(paper_summary)
    return paper_summary.summary