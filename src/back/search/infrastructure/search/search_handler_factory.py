from src.back.search.domain.search_model_name import SearchModelName
from src.back.core.application.file_context_accessor import FileContextAccessor
## command/handler
from src.back.search.application.usecases.search_command import SearchCommand
from src.back.search.application.usecases.search_command_handler import SearchCommandHandler
from src.back.search.application.ports.output.search.search_command_handler_factory import SearchCommandHandlerFactory
## preprocessor
from src.back.preprocessor.domain.preprocessor import Preprocessor
from src.back.preprocessor.domain.preprocessor_name import PreprocessorName
from src.back.preprocessor.infrastructure.preprocessor_factory import PreprocessorFactory
## embedding
from src.back.search.infrastructure.search.embedding.calculators.document_vector_calculator import DocumentVectorCalculator
from src.back.search.infrastructure.search.embedding.embedding_dependency import EmbeddingDependency
from src.back.search.infrastructure.search.embedding.embedding_dependency_resolver import EmbeddingDependencyResolver
from src.back.search.infrastructure.search.embedding.embedding_search_model import EmbeddingSearchModel
## tfidf
from src.back.search.infrastructure.search.tf_idf.tf_idf_dependency import TfIdfDependency
from src.back.search.infrastructure.search.tf_idf.tf_idf_dependency_resolver import TfIdfDependencyResolver
from src.back.search.infrastructure.search.tf_idf.tf_idf_search_model import TFIDFSearchModel
from src.back.core.application.file_context_accessor_factory import FileContextAccessorFactory


class SearchHandlerFactory(SearchCommandHandlerFactory):

    def __init__(self, file_context_accessor_factory: FileContextAccessorFactory, preprocessor_factory: PreprocessorFactory):
        self._preprocessor_factory = preprocessor_factory
        self._file_context_accessor_factory = file_context_accessor_factory


    def get_command_handler(self, command: SearchCommand) -> SearchCommandHandler:
        preprocessor_name = PreprocessorName(command.get_preprocessor())
        model_name = SearchModelName(command.get_search_model())

        preprocessor = self._preprocessor_factory.get_preprocessor(preprocessor_name)
        search_file_service = self._file_context_accessor_factory.create(model_name.value, preprocessor_name.value)

        search_handler = None
        match model_name.value:
            case "embedding": search_handler = self.build_embedding_handler(preprocessor, search_file_service)
            case "tfidf": search_handler = self.build_tfidf_handler(preprocessor, search_file_service)
        return search_handler
        

    def build_tfidf_handler(self, preprocessor: Preprocessor, search_file_service: FileContextAccessor) -> SearchCommandHandler[TFIDFSearchModel, TfIdfDependencyResolver]:
        model_dependency = TfIdfDependency(
            search_file_service.get_idf(),
            search_file_service.get_tf_idf_vectors(),
            search_file_service.get_full_vocab()
        )
        return SearchCommandHandler(TFIDFSearchModel(model_dependency),
                                    TfIdfDependencyResolver(preprocessor, search_file_service))
    

    def build_embedding_handler(self, preprocessor: Preprocessor, search_file_service: FileContextAccessor) -> SearchCommandHandler[EmbeddingSearchModel, EmbeddingDependencyResolver]:
        model_dependency = EmbeddingDependency(
            DocumentVectorCalculator(search_file_service.get_fassttext_model()),
            search_file_service.get_documents_embeddings()
        )
        return SearchCommandHandler(EmbeddingSearchModel(model_dependency),
                                    EmbeddingDependencyResolver(preprocessor, search_file_service))