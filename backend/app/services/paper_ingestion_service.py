from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.services.arxiv_services import ArxivService

class PaperIngestionService:
    def __init__(self, db: Session):
        self.db = db
        self.arxiv = ArxivService()

    def ingest_arxiv(self,query: str,start: int = 0,max_results: int = 20,) -> int:
        papers = self.arxiv.search(query=query,start=start,max_results=max_results,)
        if not papers:
            return 0
        external_ids = [paper.external_id for paper in papers]
        existing_ids = (self.db.query(Paper.external_id).filter(Paper.source == "arxiv",Paper.external_id.in_(external_ids),).all())
        existing_ids = {row[0] for row in existing_ids}
        new_papers=[]
        for paper in papers:
            if paper.external_id in existing_ids:
                continue
            db_paper = Paper(
                source="arxiv",
                external_id=paper.external_id,
                title=paper.title,
                authors=", ".join(paper.authors),
                abstract=paper.abstract,
                pdf_url=paper.pdf_url,
                publication_date=paper.published_at,
            )
            new_papers.append(db_paper)
            
        self.db.add_all(new_papers)
        self.db.commit()

        return len(new_papers)