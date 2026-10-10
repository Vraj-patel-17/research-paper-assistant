import asyncio
from collections import defaultdict
from collections.abc import AsyncIterator
from uuid import UUID

from app.schemas.rag import RetrievedChunk
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.llm_client import LLMClient
from app.services.paper_chunk_service import (
    has_fresh_chunks,
    purge_expired_chunks,
    replace_chunks,
    search_chunks,
)
from app.services.paper_processing import process_paper_pdf, chunk_pages

SNIPPET_CHARS = 200

# Stops two concurrent questions on the same uncached paper from both
# downloading the PDF and paying for embeddings (per process only).
_ingest_locks: defaultdict[UUID, asyncio.Lock] = defaultdict(asyncio.Lock)


class RAGService:
    def __init__(self, db_session):
        self.embedding_service = EmbeddingService()
        self.llm_client = LLMClient()
        self.db_session = db_session

    async def prepare_paper(
        self,
        pdf_url: str,
        paper_id: str | UUID,
    ) -> UUID:
        """Makes sure fresh chunks + embeddings are cached for the paper.

        arXiv is only contacted when nothing unexpired is cached, so repeat
        questions never trigger a PDF download.
        """
        paper_uuid = UUID(str(paper_id))

        async with _ingest_locks[paper_uuid]:
            await purge_expired_chunks(self.db_session)

            if await has_fresh_chunks(self.db_session, paper_uuid):
                return paper_uuid

            pages = await process_paper_pdf(pdf_url)
            page_chunks = chunk_pages(pages)

            if not page_chunks:
                raise ValueError("No chunks were created from the paper.")

            embeddings = await self.embedding_service.generate_chunk_embeddings(
                [text for _, text in page_chunks]
            )

            await replace_chunks(
                self.db_session,
                paper_uuid,
                [
                    (page, text, embedding)
                    for (page, text), embedding in zip(page_chunks, embeddings)
                ],
            )

        return paper_uuid

    async def retrieve_relevant_chunks(
        self,
        query: str,
        paper_id: UUID,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        query_embedding = await self.embedding_service.generate_query_embedding(query)

        return await search_chunks(
            self.db_session,
            paper_id=paper_id,
            query_embedding=query_embedding,
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
        paper_id: str | UUID,
        top_k: int = 5,
    ) -> str:
        paper_uuid = await self.prepare_paper(pdf_url, paper_id=paper_id)

        retrieved_chunks = await self.retrieve_relevant_chunks(
            query=question,
            paper_id=paper_uuid,
            top_k=top_k,
        )

        return await self.generate_answer(question=question, retrieved_chunks=retrieved_chunks)

    async def stream_answer_question(
        self,
        pdf_url: str,
        question: str,
        paper_id: str | UUID,
        top_k: int = 5,
    ) -> AsyncIterator[dict]:
        """Yields events: status, sources, then token events as they arrive."""
        yield {"type": "status", "message": "Reading the paper…"}
        paper_uuid = await self.prepare_paper(pdf_url, paper_id=paper_id)

        yield {"type": "status", "message": "Finding relevant sections…"}
        retrieved_chunks = await self.retrieve_relevant_chunks(
            query=question,
            paper_id=paper_uuid,
            top_k=top_k,
        )

        yield {
            "type": "sources",
            "sources": [
                {
                    "page": chunk.page,
                    "score": round(chunk.score, 4),
                    "snippet": chunk.text[:SNIPPET_CHARS],
                }
                for chunk in retrieved_chunks
            ],
        }

        yield {"type": "status", "message": "Writing the answer…"}
        prompt = self.build_prompt(question=question, retrieved_chunks=retrieved_chunks)

        async for token in self.llm_client.stream_text(prompt):
            yield {"type": "token", "text": token}