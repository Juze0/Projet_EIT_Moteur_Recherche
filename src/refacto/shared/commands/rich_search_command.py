from .rich_search_context_command import RichSearchContextCommand
from src.search_models.search_model import SearchModel
from src.preprocessing.preprocessor import Preprocessor

class RichSearchCommand(RichSearchContextCommand):
    
    def __init__(self, preprocessor: Preprocessor, search_model: SearchModel, query: str):
        super().__init__(preprocessor, search_model)
        self._query = query

    def get_query(self):
        return self._query
