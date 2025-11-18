from src.preprocessing.preprocessor import Preprocessor
from src.refacto.shared.service.search_file_service import SearchFileService
from src.refacto.shared.handler.dependency_resolver import DependencyResolver

class SearchModelDependencyResolver(DependencyResolver):

    def __init__(self, preprocessor: Preprocessor, search_file_service: SearchFileService):
        self._preprocessor = preprocessor
        self._search_file_service = search_file_service