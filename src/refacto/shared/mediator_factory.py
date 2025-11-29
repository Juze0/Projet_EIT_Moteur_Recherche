from src.refacto.shared.mediator import Mediator
# command
from src.refacto.shared.commands.raw_search_command import RawSearchCommand
# handlers
from src.refacto.shared.handler.enrich_command_handler import EnrichCommandHandler
from src.refacto.shared.handler.dependencies_handler import DependenciesHandler
from src.refacto.shared.handler.search_request_handler import SearchRequestHandler


def build_mediator() -> Mediator:
    mediator = Mediator()

    handler = EnrichCommandHandler()
    handler.setNext(DependenciesHandler()).setNext(SearchRequestHandler())

    mediator.register_handler(RawSearchCommand, handler)
    return mediator