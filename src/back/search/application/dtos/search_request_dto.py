from dataclasses import dataclass

@dataclass(frozen=True)
class SearchRequestDTO:
    preprocessor: str
    search_model: str
    query: str
    top_n: int
