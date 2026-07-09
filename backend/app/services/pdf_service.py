
import requests

class PDFService:

    def download_pdf(self, pdf_url: str) -> bytes:
        response = requests.get(pdf_url)
        response.raise_for_status()
        return response.content

    