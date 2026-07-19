import re
from dataclasses import dataclass
from app.models.paper_content import PaperContent
from rank_bm25 import BM25Okapi
from app.models.paperchunk import PaperChunk 
@dataclass
class RetrievedChunk:
    chunk_id: int
    chunk_index: int
    content: str
    section: str | None
    score: float

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at",
    "be", "by", "for", "from",
    "has", "have", "had",
    "in", "into", "is", "it",
    "of", "on", "or", "that",
    "the", "their", "this", "to",
    "was", "were", "will", "with",
    "what", "which", "who", "when",
    "where", "why", "how", "can",
    "could", "should", "would",
}
class RetrievalService:
       
    def tokenize(
        self,
        text: str,
    ) -> list[str]:
        tokens=re.findall(r"\b[a-zA-Z0-9]+\b",text.lower())
        return [ token for token in tokens if token not in STOP_WORDS and len(token)>2]
    
    def expand_neighbors(self,chunks:list[PaperChunk],retrieved_chunks:list[RetrievedChunk])->list[RetrievedChunk]:
        chunk_lookup = {chunk.chunk_index: chunk for chunk in chunks}
        expanded: dict[int, RetrievedChunk] = {}
        for retrieved in retrieved_chunks:
            for neighbor_index in (retrieved.chunk_index-1,retrieved.chunk_index,retrieved.chunk_index+1):
                chunk=chunk_lookup.get(neighbor_index)
                if chunk is None:
                    continue
                expanded[chunk.id] = RetrievedChunk(
                    chunk_id=chunk.id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.text,
                    section=chunk.section,
                    score=retrieved.score,)
        return sorted(expanded.values(),key=lambda chunk:chunk.chunk_index)
    def retrieve(
        self,
        paper_content: PaperContent,
        question: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        chunks = paper_content.chunks
        if not chunks:
            return []
        tokenized_chunks=[self.tokenize(chunk.text) for chunk in chunks]
        bm25=BM25Okapi(tokenized_chunks)
        question_tokens=self.tokenize(question)
        scores=bm25.get_scores(question_tokens)
        max_score = max(scores) if len(scores) > 0 else 0
        threshold = max_score * 0.2
        preferred_sections=self.get_preferred_sections(question)
        retrieved_chunks = []
        for chunk,score in zip(chunks,scores):
            if (preferred_sections and chunk.section and chunk.section.lower() in preferred_sections):
                score*=1.5
            if score<threshold:
                continue
            retrieved_chunks.append(
                RetrievedChunk(
                    chunk_id=chunk.id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.text,
                    section=chunk.section,
                    score=float(score),
                )
            )

        retrieved_chunks.sort(
            key=lambda chunk: chunk.score,
            reverse=True,
        )
        top_chunks=retrieved_chunks[:top_k]
        expanded_chunks=self.expand_neighbors(chunks,top_chunks)
        return expanded_chunks
    
    def build_context(self,chunks: list[RetrievedChunk],) -> str:
        context = []
        current_section = None
        for chunk in chunks:
            if chunk.section and chunk.section != current_section:
                context.append(f"## {chunk.section}")
                current_section = chunk.section
            context.append(chunk.content)
        return "\n\n".join(context)
    def get_preferred_sections(self, question: str) -> set[str]:
        question = question.lower()
        summary_keywords = {"summary","summarize","overview","objective",
            "purpose","goal","contribution","contributions","main idea",
            "main contribution",}

        method_keywords = {"method","approach","architecture","algorithm",
            "training","loss","optimizer","implementation",}

        if any(keyword in question for keyword in summary_keywords):
            return {"abstract", "introduction", "conclusion"}

        if any(keyword in question for keyword in method_keywords):
            return {"method", "methods", "approach"}

        return set()