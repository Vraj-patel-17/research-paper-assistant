from app.exceptions.llm_exceptions import LLMGenerationError
from app.core.config import settings
from app.core.logging import get_logger
from app.services.base_client import GeminiClient

logger = get_logger(__name__)


class LLMClient(GeminiClient):
    def __init__(self):
        super().__init__()
        self.model = settings.llm_model

    def generate_text(self, prompt: str) -> str:
        logger.info("Generating content using model '%s'.", self.model)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
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