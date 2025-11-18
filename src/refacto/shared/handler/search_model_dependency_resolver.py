from src.refacto.shared.handler.dependency_resolver import DependencyResolver

class SearchModelDependencyResolver(DependencyResolver):

    def __init__(self, preprocessor, search_file_service):
        self._preprocessor = preprocessor
        self._search_file_service = search_file_service