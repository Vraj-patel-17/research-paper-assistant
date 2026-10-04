import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rate_limiter import limiter
from app.database import SessionLocal, get_db
from app.core.security import get_current_user 
from app.models.paper import Paper  
from app.exceptions.pdf_exceptions import (
    PDFDownloadError,
    PDFExtractionError,
    EmptyPDFError,
)
from app.exceptions.llm_exceptions import LLMGenerationError
from app.schemas.rag import AskQuestionRequest, AskQuestionResponse
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/papers", tags=["rag"])


async def _get_paper_or_404(paper_id: str | UUID, db: AsyncSession) -> Paper:
    paper = await db.get(Paper, paper_id)
    if paper is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found.",
        )
    return paper


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event)}\n\n"


@router.post("/{paper_id}/ask", response_model=AskQuestionResponse)
async def ask_question(
    paper_id: str,
    body: AskQuestionRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),  # remove if this endpoint is public
) -> AskQuestionResponse:
    paper = await _get_paper_or_404(paper_id, db)

    rag_service = RAGService(db_session=db)

    try:
        answer = await rag_service.answer_question(
            pdf_url=paper.pdf_url,
            question=body.question,
            paper_id=paper_id,
            top_k=body.top_k,
        )

    except PDFDownloadError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not retrieve the paper's PDF.",
        ) from exc

    except (PDFExtractionError, EmptyPDFError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The paper's PDF could not be processed for text content.",
        ) from exc

    except LLMGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The assistant failed to generate an answer. Please try again.",
        ) from exc

    except ValueError as exc:
        # e.g. empty question after strip, or "No chunks were created"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return AskQuestionResponse(answer=answer, paper_id=paper_id)


@router.post("/{paper_id}/ask/stream")
@limiter.limit("20/minute")
async def ask_question_stream(
    request: Request,
    paper_id: UUID,
    body: AskQuestionRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    paper = await _get_paper_or_404(paper_id, db)

    # Copy what the stream needs now. The request-scoped session may be
    # closed before streaming finishes, so the stream opens its own.
    pdf_url = paper.pdf_url
    paper_key = str(paper_id)

    async def event_stream():
        try:
            async with SessionLocal() as session:
                rag_service = RAGService(db_session=session)

                async for event in rag_service.stream_answer_question(
                    pdf_url=pdf_url,
                    question=body.question,
                    paper_id=paper_key,
                    top_k=body.top_k,
                ):
                    yield _sse(event)

            yield _sse({"type": "done"})

        except PDFDownloadError:
            yield _sse({"type": "error", "message": "Could not retrieve the paper's PDF."})

        except (PDFExtractionError, EmptyPDFError):
            yield _sse({
                "type": "error",
                "message": "The paper's PDF could not be processed for text content.",
            })

        except LLMGenerationError:
            yield _sse({
                "type": "error",
                "message": "The assistant failed to generate an answer. Please try again.",
            })

        except ValueError as exc:
            yield _sse({"type": "error", "message": str(exc)})

        except Exception:
            logger.exception("Unexpected error while streaming answer")
            yield _sse({"type": "error", "message": "An unexpected error occurred."})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )