import app.models
from app.database import SessionLocal
from app.services.paper_ingestion_service import PaperIngestionService

def main():
    db = SessionLocal()

    try:
        service = PaperIngestionService(db)

        inserted = service.ingest_arxiv(
            query="cat:cs.AI",
            max_results=5,
        )

        print(f"Imported {inserted} papers.")

    finally:
        db.close()


if __name__ == "__main__":
    main()