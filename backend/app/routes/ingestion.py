from fastapi import APIRouter,Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.paper_ingestion_service import PaperIngestionService
from app.schemas.ingestion import ArxivIngestionRequest
router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"],
)
@router.post("/arxiv")
def ingest_arxiv(request: ArxivIngestionRequest,db:Session=Depends(get_db)):
    print("Creating service")
    service=PaperIngestionService(db)
    print("Calling service")
    result=service.ingest_arxiv(query=request.query,start=request.start,max_results=request.max_results)
    print("Service finished")
    return result

    