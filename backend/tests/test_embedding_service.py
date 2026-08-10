from unittest.mock import MagicMock, patch
from app.services.embeddings.embedding_service import EmbeddingService
def test_generate_embedding_success():
    mock_response = MagicMock()
    mock_response.embeddings = [
        MagicMock(values=[0.1, 0.2, 0.3])
    ]

    with patch(
        "app.services.embeddings.embedding_service.GeminiClient.__init__",
        return_value=None,
    ):
        service = EmbeddingService()

    service.client = MagicMock()
    service.client.models.embed_content.return_value = mock_response
    service.model = "test-embedding-model"

    result = service.generate_embedding("Research paper text.")

    assert result == [0.1, 0.2, 0.3]

    service.client.models.embed_content.assert_called_once_with(
        model="test-embedding-model",
        contents="Research paper text.",
    )

def test_generate_embedding_empty_response():
    mock_response = MagicMock()
    mock_response.embeddings = []

    with patch(
        "app.services.embeddings.embedding_service.GeminiClient.__init__",
        return_value=None,
    ):
        service = EmbeddingService()

    service.client = MagicMock()
    service.client.models.embed_content.return_value = mock_response
    service.model = "test-embedding-model"

    try:
        service.generate_embedding("Research paper text.")
        assert False, "Expected embedding generation to fail"
    except IndexError:
        pass