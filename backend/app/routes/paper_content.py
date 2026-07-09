from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.paper_content import PaperContentResponse
from app.services.paper_content_service import PaperContentService

router = APIRouter(
    prefix="/papers",
    tags=["Paper Content"],
)
@router.get(
    "/{paper_id}/content",
    response_model=PaperContentResponse,
)
def get_content(
    paper_id: int,
    db: Session = Depends(get_db),
):
    service = PaperContentService(db)

    content = service.get_by_paper_id(paper_id)

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Paper content not found.",
        )

    return content

@router.post(
    "/{paper_id}/content/extract",
    response_model=PaperContentResponse,
)
def extract_content(
    paper_id: int,
    db: Session = Depends(get_db),
):
    service = PaperContentService(db)

    try:
        return service.get_or_extract(paper_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )