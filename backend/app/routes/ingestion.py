from fastapi import APIRouter,Depends,Request
from app.core.rate_limiter import limiter
from app.core.security import get_current_user
from app.database import get_db
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.paper_ingestion_service import PaperIngestionService
from app.schemas.ingestion import ArxivIngestionRequest
router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"],
)
@router.post("/arxiv")
@limiter.limit("5/minute")
async def ingest_arxiv(request: Request,body: ArxivIngestionRequest,db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user)):
    service=PaperIngestionService(db)
    result=await service.ingest_arxiv(query=body.query,start=body.start,max_results=body.max_results)
    return result