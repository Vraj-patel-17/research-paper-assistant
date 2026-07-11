from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.summary import SummaryResponse
from app.services.paper_services import get_paper_by_id
from app.services.summary_services import summary_service
from app.exceptions.llm_exceptions import LLMGenerationError
from app.exceptions.pdf_exceptions import PDFDownloadError,EmptyPDFError
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
    try:
        summary = summary_service.get_or_create_summary(
            db=db,
            paper=paper,
        )
        return summary
    except PDFDownloadError:
        raise HTTPException(
            status_code=502,
            detail="Failed to download paper PDF.",
        )

    except EmptyPDFError:
        raise HTTPException(
            status_code=400,
            detail="Paper contains no extractable text.",
        )

    except LLMGenerationError:
        raise HTTPException(
            status_code=503,
            detail="Summary generation failed.",
        )

   