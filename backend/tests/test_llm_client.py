from unittest.mock import MagicMock, patch

import pytest

from app.exceptions.llm_exceptions import LLMGenerationError
from app.services.llm_client import LLMClient


@pytest.mark.asyncio
async def test_generate_text_success():
    mock_response = MagicMock()
    mock_response.text = "Generated research summary."

    with patch(
        "app.services.llm_client.GeminiClient.__init__",
        return_value=None,
    ):
        client = LLMClient()

    client.client = MagicMock()
    client.client.models.generate_content.return_value = mock_response
    client.model = "test-model"

    result = await client.generate_text("Summarize this paper.")

    assert result == "Generated research summary."

    client.client.models.generate_content.assert_called_once_with(
        model="test-model",
        contents="Summarize this paper.",
    )

@pytest.mark.asyncio
async def test_generate_text_llm_failure():
    with patch(
        "app.services.llm_client.GeminiClient.__init__",
        return_value=None,
    ):
        client = LLMClient()

    client.client = MagicMock()
    client.client.models.generate_content.side_effect = Exception(
        "Gemini API unavailable"
    )
    client.model = "test-model"

    try:
        await client.generate_text("Summarize this paper.")
        assert False, "Expected LLMGenerationError"
    except LLMGenerationError as exc:
        assert str(exc) == "Failed to generate content using the LLM."

@pytest.mark.asyncio
async def test_generate_text_empty_response():
    mock_response = MagicMock()
    mock_response.text = ""

    with patch(
        "app.services.llm_client.GeminiClient.__init__",
        return_value=None,
    ):
        client = LLMClient()

    client.client = MagicMock()
    client.client.models.generate_content.return_value = mock_response
    client.model = "test-model"

    try:
        await client.generate_text("Summarize this paper.")
        assert False, "Expected LLMGenerationError"
    except LLMGenerationError as exc:
        assert str(exc) == "The LLM returned an empty response"