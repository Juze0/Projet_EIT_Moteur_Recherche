from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.back.search.domain.search_query import SearchQuery

@dataclass(frozen=True)
class ScoredDocument:
    document_name: str
    score: float


class SearchModel(ABC):

    @abstractmethod
    def calculate_docs_to_answer_query_docs(self, search_query: SearchQuery) -> list[ScoredDocument]:
        raise NotImplementedError("This method in not implemented in the subclasses !")
