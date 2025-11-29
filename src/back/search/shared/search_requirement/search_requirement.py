from abc import ABC

class SearchRequirement(ABC):

    def __init__(self, preprocessed_query: str, top_n: int): #TODO: query peut évoluer
        self._preprocessed_query = preprocessed_query
        self._top_n = top_n

    def get_preprocessed_query(self) -> str:
        return self._preprocessed_query
    
    def get_top_n(self) -> int:
        return self._top_n