from abc import ABC, abstractmethod

from src.back.core.application.command import Command


class Handler(ABC):
    def __init__(self):
        self._next = None

    def setNext(self, handler: "Handler"):
        self._next = handler
        return self._next

    @abstractmethod
    def handle(self, command: Command):
        raise NotImplementedError("This method in not implemented !")