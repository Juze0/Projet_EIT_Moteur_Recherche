from .raw_search_context_command import RawSearchContextCommand


class RawSearchCommand(RawSearchContextCommand):
    
    def __init__(self, preprocessor: str, search_model: str, query: str):
        super().__init__(preprocessor, search_model)
        self._query = query

    def get_query(self):
        return self._query
