from typing import TypeVar, Generic

from src.back.core.application.command import Command
from src.back.search.domain.search_model import SearchModel
from src.back.preprocessor.domain.preprocessor import Preprocessor

P = TypeVar("P", Preprocessor, str)
S = TypeVar("M", SearchModel, str)

class SearchCommand(Command, Generic[P, S]):

    def __init__(self, query: str, top_n: int, preprocessor: str, search_model: str):
        self._query = query
        self._top_n = top_n
        self._preprocessor = preprocessor
        self.search_model = search_model

    def get_query(self) -> str:
        return self._query
    
    def get_top_n(self) -> int:
        return self._top_n

    def get_search_model(self) -> str:
        return self.search_model
    
    def get_preprocessor(self) -> str:
        return self._preprocessor
        