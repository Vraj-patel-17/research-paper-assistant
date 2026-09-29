from unittest.mock import AsyncMock, MagicMock

import pytest

from app.schemas.rag import EmbeddedChunk, RetrievedChunk
from app.services.rag_service import RAGService, derive_paper_id

PDF_URL = "https://example.com/paper.pdf"


@pytest.fixture
def rag_service():
    service = RAGService()

    service.embedding_service = MagicMock()
    service.llm_client = MagicMock()

    return service


@pytest.mark.asyncio
async def test_prepare_paper(rag_service, monkeypatch):
    monkeypatch.setattr(
        "app.services.rag_service.process_paper_pdf",
        AsyncMock(return_value=["page one text", "page two text"]),
    )

    monkeypatch.setattr(
        "app.services.rag_service.chunk_pages",
        MagicMock(
            return_value=[
                (1, "chunk one"),
                (2, "chunk two"),
            ]
        ),
    )

    rag_service.embedding_service.generate_and_save_chunk_embeddings = AsyncMock(
        return_value=[
            [0.1, 0.2],
            [0.3, 0.4],
        ]
    )

    result = await rag_service.prepare_paper(PDF_URL)

    assert result == [
        EmbeddedChunk(text="chunk one", embedding=[0.1, 0.2], page=1),
        EmbeddedChunk(text="chunk two", embedding=[0.3, 0.4], page=2),
    ]

    rag_service.embedding_service.generate_and_save_chunk_embeddings.assert_called_once_with(
        ["chunk one", "chunk two"],
        paper_id=derive_paper_id(PDF_URL),
        db_session=None,
    )


@pytest.mark.asyncio
async def test_prepare_paper_uses_cached_embeddings(rag_service, monkeypatch):
    rag_service.db_session = MagicMock()

    monkeypatch.setattr(
        "app.services.rag_service.process_paper_pdf",
        AsyncMock(return_value=["page one text"]),
    )

    monkeypatch.setattr(
        "app.services.rag_service.chunk_pages",
        MagicMock(return_value=[(1, "chunk one"), (2, "chunk two")]),
    )

    monkeypatch.setattr(
        "app.services.rag_service.get_stored_embeddings",
        AsyncMock(return_value=[[0.1, 0.2], [0.3, 0.4]]),
    )

    rag_service.embedding_service.generate_and_save_chunk_embeddings = AsyncMock()

    result = await rag_service.prepare_paper(PDF_URL, paper_id="paper-1")

    assert result == [
        EmbeddedChunk(text="chunk one", embedding=[0.1, 0.2], page=1),
        EmbeddedChunk(text="chunk two", embedding=[0.3, 0.4], page=2),
    ]

    rag_service.embedding_service.generate_and_save_chunk_embeddings.assert_not_called()


@pytest.mark.asyncio
async def test_prepare_paper_no_chunks(rag_service, monkeypatch):
    monkeypatch.setattr(
        "app.services.rag_service.process_paper_pdf",
        AsyncMock(return_value=[]),
    )

    monkeypatch.setattr(
        "app.services.rag_service.chunk_pages",
        MagicMock(return_value=[]),
    )

    with pytest.raises(ValueError):
        await rag_service.prepare_paper(PDF_URL)


@pytest.mark.asyncio
async def test_retrieve_relevant_chunks(rag_service, monkeypatch):
    embedded_chunks = [
        EmbeddedChunk(text="chunk one", embedding=[0.1, 0.2], page=1),
        EmbeddedChunk(text="chunk two", embedding=[0.3, 0.4], page=2),
    ]

    rag_service.embedding_service.generate_query_embedding = AsyncMock(
        return_value=[0.5, 0.6]
    )

    expected = [
        RetrievedChunk(
            text="chunk two",
            score=0.9,
            page=2,
        )
    ]

    mock_retrieve = MagicMock(return_value=expected)

    monkeypatch.setattr(
        "app.services.rag_service.retrieve_chunks",
        mock_retrieve,
    )

    result = await rag_service.retrieve_relevant_chunks(
        query="What is the paper about?",
        embedded_chunks=embedded_chunks,
        top_k=1,
    )

    assert result == expected

    rag_service.embedding_service.generate_query_embedding.assert_called_once_with(
        "What is the paper about?"
    )

    mock_retrieve.assert_called_once_with(
        query_embedding=[0.5, 0.6],
        chunks=embedded_chunks,
        top_k=1,
    )


def test_build_prompt(rag_service):
    retrieved_chunks = [
        RetrievedChunk(
            text="The model achieved 95% accuracy.",
            score=0.95,
            page=3,
        ),
        RetrievedChunk(
            text="The dataset contained 10,000 samples.",
            score=0.90,
            page=4,
        ),
    ]

    prompt = rag_service.build_prompt(
        question="What accuracy did the model achieve?",
        retrieved_chunks=retrieved_chunks,
    )

    assert "The model achieved 95% accuracy." in prompt
    assert "The dataset contained 10,000 samples." in prompt
    assert "What accuracy did the model achieve?" in prompt
    assert "[p.3]" in prompt
    assert "[p.4]" in prompt


@pytest.mark.asyncio
async def test_generate_answer(rag_service):
    retrieved_chunks = [
        RetrievedChunk(
            text="The model achieved 95% accuracy.",
            score=0.95,
            page=1,
        )
    ]

    rag_service.llm_client.generate_text = AsyncMock(
        return_value="The model achieved 95% accuracy."
    )

    result = await rag_service.generate_answer(
        question="What accuracy did the model achieve?",
        retrieved_chunks=retrieved_chunks,
    )

    assert result == "The model achieved 95% accuracy."

    rag_service.llm_client.generate_text.assert_called_once()


@pytest.mark.asyncio
async def test_answer_question(rag_service):
    embedded_chunks = [
        EmbeddedChunk(
            text="Relevant paper content.",
            embedding=[0.1, 0.2],
            page=1,
        )
    ]

    retrieved_chunks = [
        RetrievedChunk(
            text="Relevant paper content.",
            score=0.95,
            page=1,
        )
    ]

    rag_service.prepare_paper = AsyncMock(
        return_value=embedded_chunks
    )

    rag_service.retrieve_relevant_chunks = AsyncMock(
        return_value=retrieved_chunks
    )

    rag_service.generate_answer = AsyncMock(
        return_value="This is the answer."
    )

    result = await rag_service.answer_question(
        pdf_url=PDF_URL,
        question="What does the paper say?",
        top_k=5,
    )

    assert result == "This is the answer."

    rag_service.prepare_paper.assert_called_once_with(
        PDF_URL,
        paper_id=None,
    )

    rag_service.retrieve_relevant_chunks.assert_called_once_with(
        query="What does the paper say?",
        embedded_chunks=embedded_chunks,
        top_k=5,
    )

    rag_service.generate_answer.assert_called_once_with(
        question="What does the paper say?",
        retrieved_chunks=retrieved_chunks,
    )
def test_build_prompt_without_page_number(rag_service):
    retrieved_chunks = [
        RetrievedChunk(
            text="The model achieved 95% accuracy.",
            score=0.95,
        ),
    ]

    prompt = rag_service.build_prompt(
        question="What accuracy did the model achieve?",
        retrieved_chunks=retrieved_chunks,
    )

    assert "The model achieved 95% accuracy." in prompt
    assert "[p." not in prompt