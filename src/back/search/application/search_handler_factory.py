from src.back.search.domain.search_model_name import SearchModelName

from src.back.search.application.handlers.search_handler import SearchHandler
from src.back.search.application.handlers.embedding_search_handler import EmbeddingSearchHandler
from src.back.search.application.handlers.tf_idf_search_handler import TfIdfSearchHandler

class SearchHandlerFactory():

    _search_handler_map = {
        "embedding": EmbeddingSearchHandler,
        "tfidf": TfIdfSearchHandler
    }

    def get_search_handler(self, search_model_name: SearchModelName) -> SearchHandler:
        if search_model_name.value not in self._search_handler_map:
            raise ValueError(f"Search model '{search_model_name.value}' is not recognized by the factory but is known by business rule!")
        return self._search_handler_map[search_model_name.value]()