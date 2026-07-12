class PDFDownloadError(Exception):
    """Raised when a PDF cannot be downloaded."""


class PDFExtractionError(Exception):
    """Raised when text cannot be extracted from a PDF."""


class EmptyPDFError(Exception):
    """Raised when the PDF contains no extractable text."""