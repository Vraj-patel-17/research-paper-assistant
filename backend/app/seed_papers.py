import datetime
import app.models
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.paper import Paper
import traceback
def seed_papers():
    db: Session = SessionLocal()
    try:
        # Don't insert again if papers already exist
        if db.query(Paper).first():
            print("Papers already exist. Skipping seeding.")
            return
        papers = [
            Paper(
                title="Attention Is All You Need",
                authors="Ashish Vaswani, Noam Shazeer, Niki Parmar",
                abstract="Introduced the Transformer architecture for sequence modeling.",
                pdf_url="https://arxiv.org/pdf/1706.03762.pdf",
                publication_date=datetime.datetime(2017, 6, 12),
            ),
            Paper(
                title="BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
                authors="Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
                abstract="Introduced BERT for bidirectional language representation learning.",
                pdf_url="https://arxiv.org/pdf/1810.04805.pdf",
                publication_date=datetime.datetime(2018, 10, 11),
            ),
            Paper(
                title="Language Models are Few-Shot Learners",
                authors="Tom B. Brown et al.",
                abstract="Introduced GPT-3 and demonstrated few-shot learning capabilities.",
                pdf_url="https://arxiv.org/pdf/2005.14165.pdf",
                publication_date=datetime.datetime(2020, 5, 28),
            ),
        ]

        db.add_all(papers)
        db.commit()
        print(f"Successfully seeded {len(papers)} papers.")

    except Exception:
        db.rollback()
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    seed_papers()