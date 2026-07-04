import httpx
import feedparser
from app.schemas.arxiv import ArxivPaper
class ArxivService:
    BASE_URL = "http://export.arxiv.org/api/query"

    def search(self,query: str,start: int = 0,max_results: int = 20,) -> list[ArxivPaper]:
        params = {"search_query": query,"start": start,"max_results": max_results,}
        with httpx.Client(follow_redirects=True,timeout=30.0) as client:
            response = client.get(self.BASE_URL, params=params)
            response.raise_for_status()

        feed = feedparser.parse(response.text)
        papers=[]
        for entry in feed.entries:
            pdf_url = None

            for link in entry.links:
                if getattr(link, "title", None) == "pdf":
                    pdf_url = link.href
                    break

            paper = ArxivPaper(
                external_id=entry.id.split("/abs/")[-1],
                title=entry.title.strip(),
                abstract=entry.summary.strip(),
                authors=[author.name for author in entry.authors],
                published_at=entry.published,
                pdf_url=pdf_url,
                categories=[tag.term for tag in entry.tags],
            )

            papers.append(paper)

        return papers