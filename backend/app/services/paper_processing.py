import io
from urllib.parse import urlparse

import httpx
from pypdf import PdfReader

from app.exceptions.pdf_exceptions import (
    PDFDownloadError,
    PDFExtractionError,
    EmptyPDFError,
)
from app.services.arxiv_client import arxiv_client

ALLOWED_PDF_HOSTS = {"arxiv.org", "export.arxiv.org"}


def _normalize_pdf_url(pdf_url: str) -> str:
    if pdf_url.startswith("http://"):
        return "https://" + pdf_url[len("http://"):]
    return pdf_url


def _validate_pdf_url(pdf_url: str) -> None:
    parsed = urlparse(pdf_url)

    if parsed.scheme != "https":
        raise PDFDownloadError("Only https PDF URLs are allowed.")

    if parsed.hostname not in ALLOWED_PDF_HOSTS:
        raise PDFDownloadError(
            f"PDF host '{parsed.hostname}' is not an allowed source."
        )


async def download_pdf(pdf_url: str) -> bytes:
    pdf_url = _normalize_pdf_url(pdf_url)
    _validate_pdf_url(pdf_url)

    try:
        response = await arxiv_client.get(pdf_url)
    except httpx.HTTPError as exc:
        raise PDFDownloadError("Failed to download paper PDF.") from exc

    content_type = response.headers.get("content-type", "").lower()
    if "application/pdf" not in content_type:
        raise PDFDownloadError("URL did not return a PDF.")

    return response.content


def extract_pdf_pages(pdf_bytes: bytes) -> list[tuple[int, str]]:
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                pages.append((page_number, text))

    except Exception as exc:
        raise PDFExtractionError("Failed to extract text from PDF.") from exc

    if not pages:
        raise EmptyPDFError("PDF contains no extractable text.")

    return pages


def extract_pdf_text(pdf_bytes: bytes) -> str:
    return "\n".join(text for _, text in extract_pdf_pages(pdf_bytes)).strip()


async def process_paper_pdf(pdf_url: str) -> list[tuple[int, str]]:
    pdf_bytes = await download_pdf(pdf_url)
    return extract_pdf_pages(pdf_bytes)


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be greater than or equal to 0 "
            "and less than chunk_size."
        )

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def chunk_pages(
    pages: list[tuple[int, str]],
    chunk_size: int = 1200,
    overlap: int = 200,
) -> list[tuple[int, str]]:
    chunks: list[tuple[int, str]] = []

    for page_number, page_text in pages:
        for chunk in chunk_text(page_text, chunk_size=chunk_size, overlap=overlap):
            chunks.append((page_number, chunk))

    return chunks