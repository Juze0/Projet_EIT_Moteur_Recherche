from src.back.search.application.usecases.search_command import SearchCommand
from src.back.search.application.handlers.search_handler import SearchHandler
from src.back.search.application.ports.search_handler_factory import SearchHandlerFactory
## embedding (TODO à cacher derrière le container)
from src.back.search.infrastructure.searchmodel.embedding_search_model import EmbeddingSearchModel
from src.back.search.infrastructure.search_model_dependency.embedding_search_model_dependency import EmbeddingSearchModelDependency
## tfidf
from src.back.search.infrastructure.searchmodel.tf_idf_search_model import TFIDFSearchModel
from src.back.search.infrastructure.search_model_dependency.tf_idf_search_model_dependency import TfIdfSearchModelDependency

class SearchHandlerFactory(SearchHandlerFactory):

    _search_handler_map = {
        "embedding": SearchHandler[EmbeddingSearchModel, EmbeddingSearchModelDependency],
        "tfidf": SearchHandler[TFIDFSearchModel, TfIdfSearchModelDependency]
    }

    def get_command_handler(self, command: SearchCommand) -> SearchHandler:
        # TODO Dois-je utiliser les VO ?
        #if search_model_name.value not in self._search_handler_map:
        #    raise ValueError(f"Search model '{search_model_name.value}' is not recognized by the factory but is known by business rule!")
        return self._search_handler_map[search_model_name.value]()
    