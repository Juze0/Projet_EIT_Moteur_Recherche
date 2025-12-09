from src.back.core.application.mediator import Mediator
# command
from src.back.search.shared.commands.raw_search_command import RawSearchCommand
# handlers
from src.back.search.shared.handler.enrich_command_handler import EnrichCommandHandler


def build_mediator() -> Mediator:
    mediator = Mediator()

    handler = EnrichCommandHandler()

    mediator.register_handler(RawSearchCommand, handler)
    return mediator