import asyncio
from io import BytesIO

import fitz  # PyMuPDF
from app.exceptions.pdf_exceptions import PDFExtractionError,EmptyPDFError
from app.core.logging import get_logger
from app.services.paper_processing import download_pdf
logger = get_logger(__name__)
class PDFService:

    def extract_text(self, pdf_bytes: bytes) -> str:
        try:
            logger.info("Extracting text from PDF.")
            try:
                document = fitz.open(stream=BytesIO(pdf_bytes), filetype="pdf")
                pages: list[str] = []
                try:

                    for page in document:
                        text = page.get_text().strip()

                        if text:
                            pages.append(text)
                finally:
                    document.close()
            except fitz.FileDataError as e:
                logger.exception("Failed to extract text from PDF.")
                raise PDFExtractionError(str(e)) from e
            text="\n\n".join(pages)
            if not text.strip():
                logger.error("PDF contains no extractable text.")
                raise EmptyPDFError("No extractable text found.")
            
            logger.info(
                "Successfully extracted text from %d pages.",
                len(pages),
            )

            return text
        except Exception:
            logger.exception("Failed to extract PDF content")
            raise

    async def extract_from_url(self, pdf_url: str) -> str:
        pdf_bytes = await download_pdf(pdf_url)
        return await asyncio.to_thread(self.extract_text, pdf_bytes)


pdf_service = PDFService()