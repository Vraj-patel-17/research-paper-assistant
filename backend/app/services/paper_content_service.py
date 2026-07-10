from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.paper_content import PaperContent

from app.services.pdf_service import pdf_service


class PaperContentService:

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

    def get_or_create_content(
        self,
        db: Session,
        paper: Paper,
    ) -> str:

        paper_content = self.get_by_paper_id(
            db=db,
            paper_id=paper.id,
        )

        if paper_content:
            return paper_content.content

        content = pdf_service.extract_from_url(
            paper.pdf_url,
        )

        self.create(
            db=db,
            paper_id=paper.id,
            content=content,
        )

        return content


paper_content_service = PaperContentService()