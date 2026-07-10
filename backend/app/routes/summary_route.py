from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.summary import SummaryResponse
from app.services.paper_services import get_paper_by_id
from app.services.summary_services import summary_service

router = APIRouter(
    prefix="/papers",
    tags=["Summaries"],
)
@router.get(
    "/{paper_id}/summary",
    response_model=SummaryResponse,
)
def get_summary(
    paper_id: int,
    db: Session = Depends(get_db),
):

    paper =get_paper_by_id(
        db=db,
        paper_id=paper_id,
    )

    if paper is None:
        raise HTTPException(
            status_code=404,
            detail="Paper not found.",
        )

    summary = summary_service.get_or_create_summary(
        db=db,
        paper=paper,
    )

    return summary