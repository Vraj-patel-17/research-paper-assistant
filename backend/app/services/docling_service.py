from docling.document_converter import DocumentConverter
import time
from pathlib import Path
class DoclingService:
    def __init__(self):
        self.converter = DocumentConverter()

    def parse_pdf(self, pdf_path: str):
        start=time.time()
        result = self.converter.convert(pdf_path)
        print(f"{time.time()-start:.2f} seconds")
        return result.document