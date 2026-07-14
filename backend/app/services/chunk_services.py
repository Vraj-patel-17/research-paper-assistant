from dataclasses import dataclass
import re

@dataclass
class Chunk:
    index: int
    content: str

class ChunkService:

    def __init__(
        self,
        chunk_size: int = 250,
        chunk_overlap: int = 50,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(
        self,
        text: str,
    ) -> list[Chunk]:

        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        chunks = []
        current_words = []
        chunk_index = 0
        for paragraph in paragraphs:
            paragraph_words = paragraph.split()
            if len(paragraph_words) > self.chunk_size:
                if current_words:
                    chunks.append(Chunk(index=chunk_index,content=" ".join(current_words),))
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
                            ),
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
                        content=" ".join(current_words),))

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
                    content=" ".join(current_words),
                )
            )

        return chunks