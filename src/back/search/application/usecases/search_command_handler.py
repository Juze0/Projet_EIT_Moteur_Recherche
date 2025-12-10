from src.back.core.application.handler import Handler
from src.back.search.application.usecases.search_command import SearchCommand
from src.back.search.application.ports.search_handler_factory import SearchHandlerFactory

class SearchCommandHandler(Handler):

    def __init__(self, search_use_case_factory: SearchHandlerFactory):
        self._factory = search_use_case_factory

    def handle(self, command: SearchCommand):
        return self._factory.get_command_handler(command).handle(command)
