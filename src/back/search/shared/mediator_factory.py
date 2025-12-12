from src.back.core.application.mediator import Mediator

from src.back.search.application.usecases.search_command import SearchCommand
from src.back.search.application.handlers.search_handler_router import SearchHandlerRouter
from src.back.search.infrastructure.search.search_handler_factory import SearchHandlerFactory


def build_mediator() -> Mediator:
    mediator = Mediator()
    mediator.register_handler(SearchCommand, SearchHandlerRouter(SearchHandlerFactory()))
    return mediator