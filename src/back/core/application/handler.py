from src.back.search.application.commands.search_command import SearchCommand
from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self):
        self._next = None

    def setNext(self, handler: "Handler"):
        self._next = handler
        return self._next

    @abstractmethod
    def handle(self, command: SearchCommand):
        raise NotImplementedError("This method in not implemented !")