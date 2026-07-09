from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.paper_content import PaperContent
from app.services.pdf_service import PDFService

class PaperContentService:
    def __init__(self, db: Session):
        self.db = db
        self.pdf_service = PDFService()

    def get_by_paper_id(self, paper_id: int) -> PaperContent | None:
        return (
            self.db.query(PaperContent)
            .filter(PaperContent.paper_id == paper_id)
            .first())
    
    def create(self, paper_id: int, full_text: str,page_count:int) -> PaperContent:
        content = PaperContent(
            paper_id=paper_id,
            full_text=full_text,page_count=page_count,extraction_status="completed"
        )
        self.db.add(content)
        self.db.commit()
        self.db.refresh(content)

        return content
    
    def get_or_extract(self, paper_id: int) -> PaperContent:
        paper = (
            self.db.query(Paper)
            .filter(Paper.id == paper_id)
            .first()
        )
        if paper is None:
            raise ValueError("Paper not found.")
        existing = self.get_by_paper_id(paper_id)
        if existing:
            return existing
        full_text ,page_count= self.pdf_service.extract_from_url(paper.pdf_url)
        return self.create(
            paper_id=paper_id,
            full_text=full_text,
            page_count=page_count,
        )