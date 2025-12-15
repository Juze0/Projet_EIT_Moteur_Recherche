from src.back.core.application.mediator import Mediator

from src.back.core.infrastructure.local_paths_provider import LocalPathsProvider
from src.back.core.infrastructure.file_factory import FileFactory
from src.back.core.application.file_context_accessor_factory import FileContextAccessorFactory
# -- useCases
# searchCommand
from src.back.search.application.usecases.search_command import SearchCommand
from src.back.search.application.handlers.search_handler_router import SearchHandlerRouter
from src.back.search.infrastructure.search.search_handler_factory import SearchHandlerFactory
from src.back.preprocessor.infrastructure.preprocessor_factory import PreprocessorFactory
# readFileCommand
from src.back.core.application.usecases.read_file_command import ReadFileCommand
from src.back.core.application.usecases.read_file_command_handler import ReadFileCommandHandler
# TODO Faire cela au sein d'une composition root




def build_mediator() -> Mediator:
    mediator = Mediator()
    file_context_accessor_factory = FileContextAccessorFactory(LocalPathsProvider(), FileFactory())

    mediator.register_handler(SearchCommand, SearchHandlerRouter(SearchHandlerFactory(file_context_accessor_factory, PreprocessorFactory())))
    mediator.register_handler(ReadFileCommand, ReadFileCommandHandler(file_context_accessor_factory))

    return mediator