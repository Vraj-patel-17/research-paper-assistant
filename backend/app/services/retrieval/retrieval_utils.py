class RetrievalUtils:

    @staticmethod
    def is_valid_chunk(
        text: str,
        section: str | None,
    ) -> bool:
        text = text.strip()
        if len(text) < 50:
            return False
        if "arxiv:" in text.lower():
            return False
        if section and section.lower() == "references":
            return False
        return True