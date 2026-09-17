import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.services.paper_services import get_paper_by_id
from app.services.pdf_service import pdf_service
from app.services.llm_client import LLMClient
from app.prompts.summary_prompt import build_summary_prompt
from app.models.paper_summary import PaperSummary

async def generate_paper_summary(
    db: AsyncSession,
    paper_id: UUID,
) -> str:

    paper = await get_paper_by_id(db, paper_id)

    if not paper:
        raise LookupError("Paper not found")
    if not paper.pdf_url:
        raise ValueError("Paper does not have a PDF URL")

    existing_summary = (
        await db.execute(select(PaperSummary).where(PaperSummary.paper_id == paper_id))
    ).scalar_one_or_none()

    if existing_summary:
        return existing_summary.summary

    # pdf_service does blocking I/O (httpx.get + PyMuPDF parsing) —
    # offload to a thread so it doesn't stall the event loop.
    full_text = await asyncio.to_thread(pdf_service.extract_from_url, paper.pdf_url)

    prompt = build_summary_prompt(
        title=paper.title,
        full_text=full_text,
    )

    llm_client = LLMClient()
    summary_text = await llm_client.generate_text(prompt)

    paper_summary = PaperSummary(
        paper_id=paper_id,
        summary=summary_text,
    )
    db.add(paper_summary)
    await db.commit()
    await db.refresh(paper_summary)
    return paper_summary.summary

async def regenerate_paper_summary(
    db: AsyncSession,
    paper_id: UUID,
) -> str:
    paper = await get_paper_by_id(db, paper_id)

    if not paper:
        raise LookupError("Paper not found")

    if not paper.pdf_url:
        raise ValueError("Paper does not have a PDF URL")

    full_text = await asyncio.to_thread(pdf_service.extract_from_url, paper.pdf_url)

    prompt = build_summary_prompt(
        title=paper.title,
        full_text=full_text,
    )

    llm_client = LLMClient()
    summary_text = await llm_client.generate_text(prompt)

    existing_summary = (
        await db.execute(select(PaperSummary).where(PaperSummary.paper_id == paper_id))
    ).scalar_one_or_none()

    if existing_summary:
        existing_summary.summary = summary_text
    else:
        existing_summary = PaperSummary(
            paper_id=paper_id,
            summary=summary_text,
        )
        db.add(existing_summary)

    await db.commit()
    await db.refresh(existing_summary)

    return existing_summary.summary