from app.services.arxiv_services import ArxivService

service = ArxivService()

papers = service.search(query="all:transformer",max_results=3,)
for paper in papers:
    print(paper.model_dump())

