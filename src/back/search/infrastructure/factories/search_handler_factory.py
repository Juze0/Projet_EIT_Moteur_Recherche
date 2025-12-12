from src.back.preprocessor.domain.preprocessor_name import PreprocessorName
from src.back.search.domain.search_model_name import SearchModelName
from src.back.preprocessor.infrastructure.preprocessor_factory import PreprocessorFactory

from src.back.search.shared.service.search_file_service import SearchFileService

from src.back.search.infrastructure.search_model_dependency_resolver.tf_idf_dependency_resolver import TfIdfDependencyResolver
from src.back.search.infrastructure.search_model_dependency_resolver.embedding_dependency_resolver import EmbeddingDependencyResolver
from src.back.preprocessor.domain.preprocessor import Preprocessor

from src.back.search.embeddings.calculators.document_vector_calculator import DocumentVectorCalculator

from src.back.search.application.usecases.search_command import SearchCommand
from src.back.search.application.usecases.search_command_handler import SearchCommandHandler
from src.back.search.application.ports.search.search_command_handler_factory import SearchCommandHandlerFactory
## embedding (TODO à cacher derrière le container)
from src.back.search.infrastructure.searchmodel.embedding_search_model import EmbeddingSearchModel
from src.back.search.infrastructure.search.dependencies.embedding_dependency import EmbeddingDependency
## tfidf
from src.back.search.infrastructure.searchmodel.tf_idf_search_model import TFIDFSearchModel
from src.back.search.infrastructure.search.dependencies.tf_idf_dependency import TfIdfDependency

class SearchHandlerFactory(SearchCommandHandlerFactory):

    def __init__(self):
        self._preprocessor_factory = PreprocessorFactory()


    def get_command_handler(self, command: SearchCommand) -> SearchCommandHandler:
        preprocessor_name = PreprocessorName(command.get_preprocessor())
        model_name = SearchModelName(command.get_search_model())

        preprocessor = self._preprocessor_factory.get_preprocessor(preprocessor_name)
        search_file_service = SearchFileService(model_name.value, preprocessor_name.value)

        search_handler = None
        match model_name.value:
            case "embedding": search_handler = self.build_embedding_handler(preprocessor, search_file_service)
            case "tfidf": search_handler = self.build_tfidf_handler(preprocessor, search_file_service)
        return search_handler
        

    def build_tfidf_handler(self, preprocessor: Preprocessor, search_file_service: SearchFileService) -> SearchCommandHandler[TFIDFSearchModel, TfIdfDependencyResolver]:
        model_dependency = TfIdfDependency(
            search_file_service.get_idf(),
            search_file_service.get_tf_idf_vectors(),
            search_file_service.get_full_vocab()
        )
        return SearchCommandHandler(TFIDFSearchModel(model_dependency),
                                    TfIdfDependencyResolver(preprocessor, search_file_service))
    

    def build_embedding_handler(self, preprocessor: Preprocessor, search_file_service: SearchFileService) -> SearchCommandHandler[EmbeddingSearchModel, EmbeddingDependencyResolver]:
        model_dependency = EmbeddingDependency(
            DocumentVectorCalculator(search_file_service.get_fassttext_model()),
            search_file_service.get_documents_embeddings()
        )
        return SearchCommandHandler(EmbeddingSearchModel(model_dependency),
                                    EmbeddingDependencyResolver(preprocessor, search_file_service))