from src.back.search.shared.commands.command import Command
from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self):
        self._next = None

    def setNext(self, handler: "Handler"):
        self._next = handler
        return self._next

    @abstractmethod
    def handle(self, command: Command):
        raise NotImplementedError("This method in not implemented !")