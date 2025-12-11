class SearchState:
    def __init__(self):
        self._preprocessor = "spacy"
        self._model = "embedding"
        self._last_query = None
        self._search_history = []

    def get_preprocessor(self):
        return self._preprocessor

    def get_model(self):
        return self._model

    def get_last_query(self):
        return self._last_query

    def get_search_history(self):
        return list(self._search_history)

    def set_preprocessor(self, preprocessor: str):
        self._preprocessor = preprocessor

    def set_model(self, model: str):
        self._model = model

    def set_last_query(self, query: str):
        self._last_query = query
        self._search_history.append(query)

