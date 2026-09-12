import io

import httpx
from pypdf import PdfReader

from app.exceptions import (
    PDFDownloadError,
    PDFExtractionError,
    EmptyPDFError,
)


async def download_pdf(pdf_url: str) -> bytes:
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(pdf_url)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise PDFDownloadError("Failed to download paper PDF.") from exc

    return response.content


def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

    except Exception as exc:
        raise PDFExtractionError("Failed to extract text from PDF.") from exc

    extracted_text = "\n".join(pages).strip()

    if not extracted_text:
        raise EmptyPDFError("PDF contains no extractable text.")

    return extracted_text


async def process_paper_pdf(pdf_url: str) -> str:
    pdf_bytes = await download_pdf(pdf_url)
    return extract_pdf_text(pdf_bytes)

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