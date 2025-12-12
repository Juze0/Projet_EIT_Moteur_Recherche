from abc import ABC, abstractmethod

from src.back.search.application.usecases.search_command import SearchCommand
from src.back.search.application.usecases.search_command_handler import SearchCommandHandler

class SearchCommandHandlerFactory(ABC):

    @abstractmethod
    def get_command_handler(self, command: SearchCommand) -> SearchCommandHandler:
        raise NotImplementedError("This method in not implemented !")
