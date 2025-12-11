from src.back.core.application.mediator import Mediator

from src.back.search.application.usecases.search_command import SearchCommand
from src.back.search.application.usecases.search_command_handler import SearchCommandHandler
from src.back.search.infrastructure.factories.search_handler_factory import SearchHandlerFactory


def build_mediator() -> Mediator:
    mediator = Mediator()
    mediator.register_handler(SearchCommand, SearchCommandHandler(SearchHandlerFactory()))
    return mediator