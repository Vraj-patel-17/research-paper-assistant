from dataclasses import dataclass
import re

@dataclass
class Chunk:
    index: int
    content: str
    section : str | None=None

class ChunkService:
    SECTION_PATTERN = re.compile(
        r"^(\d+(\.\d+)*)?\s*[A-Z][A-Za-z0-9\s\-/:]{2,80}$"
    )
    def __init__(
        self,
        chunk_size: int = 250,
        chunk_overlap: int = 50,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def is_heading(self,text:str)->bool:
        words=text.split()
        if len(words) > 10:
            return False
        if text.endswith("."):
            return False
        return bool(self.SECTION_PATTERN.match(text))

    def chunk_text(
        self,
        text: str,
    ) -> list[Chunk]:

        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        chunks = []
        current_words = []
        chunk_index = 0
        current_section=None
        for paragraph in paragraphs:
            if self.is_heading(paragraph):
                current_section = paragraph
                continue
            paragraph_words = paragraph.split()
            if len(paragraph_words) > self.chunk_size:
                if current_words:
                    chunks.append(Chunk(index=chunk_index,content=" ".join(current_words),section=current_section))
                    chunk_index += 1
                    current_words = []
                start = 0
                while start < len(paragraph_words):
                    end = start + self.chunk_size
                    chunks.append(
                        Chunk(
                            index=chunk_index,
                            content=" ".join(
                                paragraph_words[start:end]
                            ),section=current_section
                        )
                    )
                    chunk_index += 1
                    start += (self.chunk_size - self.chunk_overlap)
                continue

            if (
                len(current_words)
                + len(paragraph_words)
                <= self.chunk_size
            ):
                current_words.extend(paragraph_words)

            else:
                chunks.append(Chunk(
                        index=chunk_index,
                        content=" ".join(current_words),section=current_section))

                chunk_index += 1
                overlap = (
                    current_words[-self.chunk_overlap :]
                    if current_words
                    else []
                )
                current_words = overlap + paragraph_words

        if current_words:
            chunks.append(
                Chunk(
                    index=chunk_index,
                    content=" ".join(current_words),section=current_section
                )
            )

        return chunks