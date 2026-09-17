import hashlib

from app.schemas.rag import EmbeddedChunk, RetrievedChunk
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.llm_client import LLMClient
from app.services.paper_processing import process_paper_pdf, chunk_pages
from app.services.retrieval_service import retrieve_chunks
from app.services.paper_chunk_service import get_stored_embeddings


def derive_paper_id(pdf_url: str) -> str:
    return hashlib.sha256(pdf_url.encode("utf-8")).hexdigest()


class RAGService:
    def __init__(self, db_session=None):
        self.embedding_service = EmbeddingService()
        self.llm_client = LLMClient()
        self.db_session = db_session

    async def prepare_paper(
        self,
        pdf_url: str,
        paper_id: str | None = None,
    ) -> list[EmbeddedChunk]:
        paper_id = paper_id or derive_paper_id(pdf_url)

        pages = await process_paper_pdf(pdf_url)
        page_chunks = chunk_pages(pages)

        if not page_chunks:
            raise ValueError("No chunks were created from the paper.")

        texts = [text for _, text in page_chunks]

        cached_embeddings: list[list[float]] = []
        if self.db_session is not None:
            cached_embeddings = await get_stored_embeddings(self.db_session, paper_id)

        if cached_embeddings and len(cached_embeddings) == len(texts):
            embeddings = cached_embeddings
        else:
            embeddings = await self.embedding_service.generate_and_save_chunk_embeddings(
                texts, paper_id=paper_id, db_session=self.db_session
            )

        return [
            EmbeddedChunk(text=text, embedding=embedding, page=page_number)
            for (page_number, text), embedding in zip(page_chunks, embeddings)
        ]

    async def retrieve_relevant_chunks(
        self,
        query: str,
        embedded_chunks: list[EmbeddedChunk],
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        query_embedding = await self.embedding_service.generate_query_embedding(query)

        return retrieve_chunks(
            query_embedding=query_embedding,
            chunks=embedded_chunks,
            top_k=top_k,
        )

    def build_prompt(
        self,
        question: str,
        retrieved_chunks: list[RetrievedChunk],
    ) -> str:
        context = "\n\n".join(
            f"[p.{chunk.page}] {chunk.text}" if chunk.page else chunk.text
            for chunk in retrieved_chunks
        )

        return (
            "You are a research paper assistant.\n\n"
            "Answer the user's question using only the provided paper context.\n\n"
            "If the context does not contain enough information to answer the "
            "question, say that the information is not available in the "
            "provided context.\n\n"
            f"Paper context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            "Answer:"
        )

    async def generate_answer(
        self,
        question: str,
        retrieved_chunks: list[RetrievedChunk],
    ) -> str:
        prompt = self.build_prompt(question=question, retrieved_chunks=retrieved_chunks)
        return await self.llm_client.generate_text(prompt)

    async def answer_question(
        self,
        pdf_url: str,
        question: str,
        paper_id: str | None = None,
        top_k: int = 5,
    ) -> str:
        embedded_chunks = await self.prepare_paper(pdf_url, paper_id=paper_id)

        retrieved_chunks = await self.retrieve_relevant_chunks(
            query=question,
            embedded_chunks=embedded_chunks,
            top_k=top_k,
        )

        return await self.generate_answer(question=question, retrieved_chunks=retrieved_chunks)