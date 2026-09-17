from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.summary import SummaryResponse
from app.services.summary_services import generate_paper_summary,regenerate_paper_summary


router = APIRouter(
    prefix="/papers",
    tags=["Summary"],
)


@router.get(
    "/{paper_id}/summary",
    response_model=SummaryResponse,
)
async def get_paper_summary(
    paper_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        summary = await generate_paper_summary(
            db=db,
            paper_id=paper_id,
        )

    except LookupError:
        raise HTTPException(
            status_code=404,
            detail="No paper found",
        )

    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Paper does not have a PDF URL",
        )

    return SummaryResponse(
        paper_id=paper_id,
        summary=summary,
    )
@router.post(
    "/{paper_id}/summary/regenerate",
    response_model=SummaryResponse,
)
async def regenerate_summary(
    paper_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        summary = await regenerate_paper_summary(
            db=db,
            paper_id=paper_id,
        )
    except LookupError:
        raise HTTPException(
            status_code=404,
            detail="No paper found",
        )
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Paper does not have a PDF URL",
        )

    return SummaryResponse(
        paper_id=paper_id,
        summary=summary,
    )