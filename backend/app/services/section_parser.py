from dataclasses import dataclass

@dataclass
class ParsedSection:
    title: str
    content: str
    order_index: int