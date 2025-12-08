from typing import TypeVar, Generic

from src.back.core.application.command import Command
from src.back.search.domain.search_model import SearchModel
from src.back.preprocessing.preprocessor import Preprocessor

P = TypeVar("P", Preprocessor, str)
S = TypeVar("M", SearchModel, str)

class SearchCommand(Command, Generic[P, S]):

    def __init__(self, preprocessor: P, search_model: S):
        self._preprocessor = preprocessor
        self.search_model = search_model

    def get_search_model(self) -> S:
        return self.search_model
    
    def get_preprocessor(self) -> P:
        return self._preprocessor
        