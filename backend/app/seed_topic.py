from app.database import SessionLocal
from app.models.topic import Topic

TOPICS = [
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Robotics",
    "Reinforcement Learning",
    "Generative AI",
    "Graph Neural Networks",
    "Quantum Computing",
    "Cybersecurity",
    "Data Science",
]

def seed_topics():
    db = SessionLocal()

    try:
        for topic_name in TOPICS:
            exists = (
                db.query(Topic)
                .filter(Topic.name == topic_name)
                .first()
            )

            if not exists:
                db.add(Topic(name=topic_name))

        db.commit()
        print("Topics seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_topics()