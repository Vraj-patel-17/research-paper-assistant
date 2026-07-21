
from app.services.embeddings.embedding_service import EmbeddingService
embedding_service = EmbeddingService()
vector = embedding_service.generate_embedding(
    "This paper proposes a deep learning method."
)

print(len(vector))
print(vector[:5])