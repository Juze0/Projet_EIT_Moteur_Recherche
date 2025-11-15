from .rich_search_context_command import RichSearchContextCommand
from src.search_models.search_model import SearchModel
from src.preprocessing.preprocessor import Preprocessor
from src.refacto.shared.handler.dependencies_handler import DependenciesHandler

class RichSearchCommand(RichSearchContextCommand):
    
    def __init__(self, preprocessor: Preprocessor, search_model: SearchModel, dependencies_handler:DependenciesHandler, query: str):
        super().__init__(preprocessor, search_model)
        self._dependencies_handler = dependencies_handler
        self._query = query

    
    def get_dependencies_handler(self) -> DependenciesHandler:
        return self._dependencies_handler


    def get_query(self):
        return self._query
