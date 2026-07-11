from io import BytesIO

import fitz  # PyMuPDF
import httpx
from app.exceptions.pdf_exceptions import PDFDownloadError,PDFExtractionError,EmptyPDFError
from app.core.logging import get_logger
from app.core.config import settings
logger = get_logger(__name__)
class PDFService:
    

    def download_pdf(self, pdf_url: str) -> bytes:
        logger.info("Downloading PDF from %s",pdf_url)
        try:
            response = httpx.get(
                pdf_url,
                timeout=settings.PDF_TIMEOUT,
                follow_redirects=True,)
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.exception("Failed to download PDF.")
            raise PDFDownloadError(f"Failed to download PDF from '{pdf_url}'.") from e
        content_type=response.headers.get("content-type","").lower()
        if "application/pdf" not in content_type:
            logger.error("Invalid content type received: %s",content_type,)
            raise PDFDownloadError(f"URL did not return a PDF.")
        logger.info("PDF downloaded successfully.")
        return response.content

    def extract_text(self, pdf_bytes: bytes) -> str:
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

    def extract_from_url(self, pdf_url: str) -> str:
        pdf_bytes = self.download_pdf(pdf_url)
        return self.extract_text(pdf_bytes)


pdf_service = PDFService()