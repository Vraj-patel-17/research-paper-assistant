from sqlalchemy.orm import Session

from app.models.summary import Summary
from app.schemas.summary import SummaryCreate


class SummaryService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_paper_id(self, paper_id: int) -> Summary | None:
        return (
            self.db.query(Summary)
            .filter(Summary.paper_id == paper_id)
            .first()
        )

    def create(
        self,
        paper_id: int,
        summary: SummaryCreate,
        model_name: str | None = None,
    ) -> Summary:
        db_summary = Summary(
            paper_id=paper_id,
            summary_text=summary.summary_text,
            model_name=model_name,
        )

        self.db.add(db_summary)
        self.db.commit()
        self.db.refresh(db_summary)

        return db_summary

    def update(
        self,
        db_summary: Summary,
        summary_text: str,
        model_name: str | None = None,
    ) -> Summary:
        db_summary.summary_text = summary_text
        db_summary.model_name = model_name

        self.db.commit()
        self.db.refresh(db_summary)

        return db_summary

    def delete(self, db_summary: Summary):
        self.db.delete(db_summary)
        self.db.commit()