from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.paper_content import PaperContent
from app.models.paperchunk import PaperChunk
from app.services.pdf_service import pdf_service
from app.services.chunk_services import ChunkService

class PaperContentService:
    def __init__(self):
        self.chunk_service = ChunkService()

    def get_by_paper_id(
        self,
        db: Session,
        paper_id: int,
    ) -> PaperContent | None:
        return (
            db.query(PaperContent)
            .filter(PaperContent.paper_id == paper_id)
            .first()
        )

    def create(
        self,
        db: Session,
        paper_id: int,
        content: str,
    ) -> PaperContent:

        paper_content = PaperContent(
            paper_id=paper_id,
            content=content,
        )

        db.add(paper_content)
        db.commit()
        db.refresh(paper_content)

        return paper_content
    
    def create_chunks(
    self,
    db: Session,
    paper_content: PaperContent,) -> None:
        existing_chunks = (
    db.query(PaperChunk)
    .filter(PaperChunk.paper_content_id == paper_content.id)
    .first()
)
        if existing_chunks:
            return
        chunks = self.chunk_service.chunk_text(
            paper_content.content,
        )
        chunk_objects = [
            PaperChunk(
                paper_content_id=paper_content.id,
                chunk_index=chunk.index,
                text=chunk.content,
                section=chunk.section
            )
            for  chunk in chunks
        ]

        db.add_all(chunk_objects)
        db.commit()

    def get_or_create_content(
        self,
        db: Session,
        paper: Paper,
    ) -> PaperContent:

        paper_content = self.get_by_paper_id(
            db=db,
            paper_id=paper.id,
        )
        if paper_content:
            return paper_content

        content = pdf_service.extract_from_url(
            paper.pdf_url,
        )
        content = content.replace("\x00", "")
        paper_content=self.create(db=db,paper_id=paper.id,content=content)
        self.create_chunks(db=db,paper_content=paper_content)
        
        return paper_content


paper_content_service = PaperContentService()