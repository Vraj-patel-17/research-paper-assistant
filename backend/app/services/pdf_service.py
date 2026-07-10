from io import BytesIO

import fitz  # PyMuPDF
import httpx

class PDFService:
    TIMEOUT = 30

    def download_pdf(self, pdf_url: str) -> bytes:
        response = httpx.get(
            pdf_url,
            timeout=self.TIMEOUT,
            follow_redirects=True,
        )
        response.raise_for_status()

        return response.content

    def extract_text(self, pdf_bytes: bytes) -> str:
        document = fitz.open(stream=BytesIO(pdf_bytes), filetype="pdf")

        pages: list[str] = []

        try:
            for page in document:
                text = page.get_text().strip()

                if text:
                    pages.append(text)

        finally:
            document.close()

        return "\n\n".join(pages)

    def extract_from_url(self, pdf_url: str) -> str:
        pdf_bytes = self.download_pdf(pdf_url)
        return self.extract_text(pdf_bytes)


pdf_service = PDFService()