from dataclasses import dataclass

@dataclass
class SearchRequestDTO:
    preprocessor: str
    search_model: str
    query: str
