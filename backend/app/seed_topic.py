from app.database import SessionLocal
from app.models.topic import Topic

TOPICS = [
    ("Machine Learning", "machine-learning"),
    ("Deep Learning", "deep-learning"),
    ("Natural Language Processing", "nlp"),
    ("Computer Vision", "computer-vision"),
    ("Robotics", "robotics"),
    ("Reinforcement Learning", "reinforcement-learning"),
    ("Generative AI", "generative-ai"),
    ("Graph Neural Networks", "graph-neural-networks"),
    ("Quantum Computing", "quantum-computing"),
    ("Cybersecurity", "cybersecurity"),
    ("Data Science", "data-science"),
]

def seed_topics():
    db = SessionLocal()

    try:
        for topic_name,slug in TOPICS:
            exists = (
                db.query(Topic)
                .filter(Topic.slug==slug)
                .first()
            )

            if not exists:
                db.add(Topic(name=topic_name,slug=slug))

        db.commit()
        print("Topics seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_topics()