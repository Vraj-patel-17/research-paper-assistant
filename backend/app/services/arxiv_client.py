import asyncio
import time

import httpx

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class ArxivClient:
    
    def __init__(self, min_interval: float):
        self._min_interval = min_interval
        self._lock = asyncio.Lock()
        self._last_finished = 0.0

    async def get(
        self,
        url: str,
        *,
        params: dict | None = None,
    ) -> httpx.Response:
        async with self._lock:
            wait = self._min_interval - (time.monotonic() - self._last_finished)
            if wait > 0:
                await asyncio.sleep(wait)

            try:
                async with httpx.AsyncClient(
                    headers={"User-Agent": settings.arxiv_user_agent},
                    follow_redirects=True,
                    timeout=settings.PDF_TIMEOUT,
                ) as client:
                    logger.info("arXiv request: %s", url)
                    response = await client.get(url, params=params)
            finally:
                self._last_finished = time.monotonic()

        response.raise_for_status()
        return response


arxiv_client = ArxivClient(min_interval=settings.arxiv_min_interval_seconds)