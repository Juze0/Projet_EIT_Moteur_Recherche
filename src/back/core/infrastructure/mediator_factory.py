from src.back.core.application.mediator import Mediator

from src.back.search.application.usecases.search_command import SearchCommand
from src.back.search.application.handlers.search_handler_router import SearchHandlerRouter
from src.back.search.infrastructure.search.search_handler_factory import SearchHandlerFactory
# TODO Faire cela au sein d'une composition root
from src.back.core.infrastructure.file_factory import FileFactory
from src.back.core.infrastructure.local_paths_provider import LocalPathsProvider
from src.back.preprocessor.infrastructure.preprocessor_factory import PreprocessorFactory

from src.back.core.application.file_context_accessor_factory import FileContextAccessorFactory


def build_mediator() -> Mediator:
    mediator = Mediator()
    file_context_accessor_factory = FileContextAccessorFactory(LocalPathsProvider(), FileFactory())
    mediator.register_handler(SearchCommand, SearchHandlerRouter(SearchHandlerFactory(file_context_accessor_factory, PreprocessorFactory())))
    return mediator