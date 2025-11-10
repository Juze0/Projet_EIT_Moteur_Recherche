from src.shared.command import Command
from abc import abstractmethod

class BaseHandler():
    def __init__(self):
        self._next = None

    def setNext(self, handler):
        self._next = handler

    @abstractmethod
    def handle(self, command: Command):
        raise NotImplementedError("This method in not implemented in the subclasses !")