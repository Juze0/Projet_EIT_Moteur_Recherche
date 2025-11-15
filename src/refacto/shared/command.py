from abc import ABC

class Command(ABC):

    def __init__(self, model: str, preprocessor: str, query: str):
        self._model = model
        self._preprocessor = preprocessor
        self._query = query

    def get_model(self) -> str:
        return self._model
    
    def get_preprocessor(self) -> str:
        return self._preprocessor
    
    def get_query(self) -> str:
        return self._query
        