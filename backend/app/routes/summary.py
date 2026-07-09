from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.summary import SummaryResponse
from app.services.summary_services import SummaryService

router = APIRouter(
    prefix="/papers",
    tags=["Summaries"],
)
@router.get("/{paper_id}/summary", response_model=SummaryResponse)
def get_summary(
    paper_id: int,
    db: Session = Depends(get_db),
):
    summary_service = SummaryService(db)

    summary = summary_service.get_by_paper_id(paper_id)

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="Summary not found",
        )

    return summary
@router.post("/{paper_id}/summary", response_model=SummaryResponse)
def generate_summary(
    paper_id: int,
    db: Session = Depends(get_db),
):
    service = SummaryService(db)

    try:
        return service.generate_summary(paper_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )