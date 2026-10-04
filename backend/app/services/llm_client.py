import asyncio
from collections.abc import AsyncIterator

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.exceptions.llm_exceptions import LLMGenerationError
from app.core.config import settings
from app.core.logging import get_logger
from app.services.base_client import GeminiClient
from google.genai.errors import ServerError

logger = get_logger(__name__)


class LLMClient(GeminiClient):
    def __init__(self):
        super().__init__()
        self.model = settings.llm_model

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(ServerError),
        reraise=True,
    )
    def _generate_text_sync(self, prompt: str) -> str:
        logger.info("Generating content using model '%s'.", self.model)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
        except ServerError:
            logger.warning("Gemini server error, will retry if attempts remain.")
            raise
        except Exception as exc:
            logger.exception("LLM generation failed.")
            raise LLMGenerationError(
                "Failed to generate content using the LLM."
            ) from exc

        if not response.text:
            logger.error("LLM returned an empty response.")
            raise LLMGenerationError("The LLM returned an empty response")

        logger.info("Content generated successfully.")
        return response.text.strip()

    async def generate_text(self, prompt: str) -> str:
        return await asyncio.to_thread(self._generate_text_sync, prompt)

    async def stream_text(self, prompt: str) -> AsyncIterator[str]:
        """Yields text fragments as Gemini generates them.

        No retry here: once tokens have been sent to the browser, retrying
        would duplicate text. Failures surface as LLMGenerationError.
        """
        logger.info("Streaming content using model '%s'.", self.model)
        emitted = False

        try:
            stream = await self.client.aio.models.generate_content_stream(
                model=self.model,
                contents=prompt,
            )
            async for chunk in stream:
                if chunk.text:
                    emitted = True
                    yield chunk.text
        except Exception as exc:
            logger.exception("LLM streaming failed.")
            raise LLMGenerationError(
                "Failed to stream content using the LLM."
            ) from exc

        if not emitted:
            logger.error("LLM returned an empty streamed response.")
            raise LLMGenerationError("The LLM returned an empty response")

        logger.info("Content streamed successfully.")