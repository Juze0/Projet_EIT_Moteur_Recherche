from src.back.search.domain.search_model_name import SearchModelName

from src.back.search.application.handlers.search_handler import SearchHandler
## embedding (TODO à cacher derrière le container)
from src.back.search.infrastructure.searchmodel.embedding_search_model import EmbeddingSearchModel
from src.back.search.infrastructure.search_model_dependency.embedding_search_model_dependency import EmbeddingSearchModelDependency
## tfidf
from src.back.search.infrastructure.searchmodel.tf_idf_search_model import TFIDFSearchModel
from src.back.search.infrastructure.search_model_dependency.tf_idf_search_model_dependency import TfIdfSearchModelDependency

class SearchHandlerFactory():

    _search_handler_map = {
        "embedding": SearchHandler[EmbeddingSearchModel, EmbeddingSearchModelDependency],
        "tfidf": SearchHandler[TFIDFSearchModel, TfIdfSearchModelDependency]
    }

    def get_search_handler(self, search_model_name: SearchModelName) -> SearchHandler:
        if search_model_name.value not in self._search_handler_map:
            raise ValueError(f"Search model '{search_model_name.value}' is not recognized by the factory but is known by business rule!")
        return self._search_handler_map[search_model_name.value]()
    