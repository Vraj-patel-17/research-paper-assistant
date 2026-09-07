from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.summary import SummaryResponse
from app.services.summary_services import generate_paper_summary


router = APIRouter(
    prefix="/papers",
    tags=["Summary"],
)


@router.get(
    "/{paper_id}/summary",
    response_model=SummaryResponse,
)
def get_paper_summary(
    paper_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        summary = generate_paper_summary(
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