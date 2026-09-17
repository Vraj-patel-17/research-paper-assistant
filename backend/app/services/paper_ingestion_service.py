from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.paper import Paper
from app.services.arxiv_services import ArxivService
from app.services.topic_service import TopicService

class PaperIngestionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.arxiv = ArxivService()

    async def ingest_arxiv(self, query: str, start: int = 0, max_results: int = 20) -> dict:
        papers = self.arxiv.search(query=query, start=start, max_results=max_results)
        topic_service = TopicService(self.db)
        if not papers:
            return {"total": 0, "imported": 0, "skipped": 0}

        external_ids = [paper.external_id for paper in papers]
        result = await self.db.execute(
            select(Paper.external_id).where(
                Paper.source == "arxiv",
                Paper.external_id.in_(external_ids),
            )
        )
        existing_ids = {row[0] for row in result.all()}

        new_papers = []
        for paper in papers:
            if paper.external_id in existing_ids:
                continue
            db_paper = Paper(
                source="arxiv",
                external_id=paper.external_id,
                title=paper.title,
                authors=", ".join(paper.authors),
                abstract=paper.abstract,
                pdf_url=str(paper.pdf_url),
                publication_date=paper.published_at,
            )
            new_papers.append(db_paper)

        total = len(papers)
        imported = len(new_papers)
        skipped = total - imported

        self.db.add_all(new_papers)
        await self.db.commit()

        for paper in new_papers:
            await self.db.refresh(paper)

        for paper in new_papers:
            await topic_service.assign_topics(paper)

        return {
            "total": total,
            "imported": imported,
            "skipped": skipped,
        }