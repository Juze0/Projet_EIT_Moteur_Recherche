from abc import ABC, abstractmethod

from src.back.search.application.usecases.search_command import SearchCommand
from src.back.core.application.handler import Handler

class SearchHandlerFactory(ABC):

    @abstractmethod
    def get_command_handler(self, command: SearchCommand) -> Handler:
        raise NotImplementedError("This method in not implemented !")
