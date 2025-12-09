from .rich_search_context_command import RichSearchContextCommand
from src.back.search.domain.search_model import SearchModel
from src.back.preprocessor.domain.preprocessor import Preprocessor

from src.back.search.shared.service.search_file_service import SearchFileService

class RichSearchCommand(RichSearchContextCommand):
    
    def __init__(self, preprocessor: Preprocessor, search_model: SearchModel, search_file_service: SearchFileService,  query: str):
        super().__init__(preprocessor, search_model)
        self._search_file_service = search_file_service
        self._query = query

    def get_search_file_service(self) -> SearchFileService:
        return self._search_file_service

    def get_query(self):
        return self._query
