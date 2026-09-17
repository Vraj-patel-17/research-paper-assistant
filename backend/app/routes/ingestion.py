from fastapi import APIRouter,Depends
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.paper_ingestion_service import PaperIngestionService
from app.schemas.ingestion import ArxivIngestionRequest
router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"],
)
@router.post("/arxiv")
async def ingest_arxiv(request: ArxivIngestionRequest,db:AsyncSession=Depends(get_db)):
    service=PaperIngestionService(db)
    result=await service.ingest_arxiv(query=request.query,start=request.start,max_results=request.max_results)
    return result