import math

from app.schemas.rag import EmbeddedChunk, RetrievedChunk


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same dimensions.")

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)

def retrieve_chunks(
    query_embedding: list[float],
    chunks: list[EmbeddedChunk],
    top_k: int = 5,
) -> list[RetrievedChunk]:

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    scored_chunks = [
        (
            cosine_similarity(query_embedding, chunk.embedding),
            chunk,
        )
        for chunk in chunks
    ]

    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
    RetrievedChunk(
        text=chunk.text,
        score=score,
    )
    for score, chunk in scored_chunks[:top_k]
]