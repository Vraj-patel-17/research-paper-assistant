from app.schemas.rag import EmbeddedChunk, RetrievedChunk
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.llm_client import LLMClient
from app.services.paper_processing import process_paper_pdf, chunk_text
from app.services.retrieval_service import retrieve_chunks


class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.llm_client = LLMClient()

    async def prepare_paper(
        self,
        pdf_url: str,
    ) -> list[EmbeddedChunk]:
        text = await process_paper_pdf(pdf_url)

        chunks = chunk_text(text)

        if not chunks:
            raise ValueError("No chunks were created from the paper.")

        embeddings = self.embedding_service.generate_chunk_embeddings(
            chunks
        )

        return [
            EmbeddedChunk(
                text=chunk,
                embedding=embedding,
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]

    def retrieve_relevant_chunks(
        self,
        query: str,
        embedded_chunks: list[EmbeddedChunk],
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        query_embedding = (
            self.embedding_service.generate_query_embedding(query)
        )

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
            chunk.text
            for chunk in retrieved_chunks
        )

        return f"""
                    You are a research paper assistant.

                    Answer the user's question using only the provided paper context.

                    If the context does not contain enough information to answer the question,
                    say that the information is not available in the provided context.

                    Paper context:
                    {context}

                    Question:
                    {question}

                    Answer:
                    """.strip()

    def generate_answer(
        self,
        question: str,
        retrieved_chunks: list[RetrievedChunk],
    ) -> str:
        prompt = self.build_prompt(
            question=question,
            retrieved_chunks=retrieved_chunks,
        )

        return self.llm_client.generate_text(prompt)

    async def answer_question(
        self,
        pdf_url: str,
        question: str,
        top_k: int = 5,
    ) -> str:
        embedded_chunks = await self.prepare_paper(pdf_url)

        retrieved_chunks = self.retrieve_relevant_chunks(
            query=question,
            embedded_chunks=embedded_chunks,
            top_k=top_k,
        )

        return self.generate_answer(
            question=question,
            retrieved_chunks=retrieved_chunks,
        )

