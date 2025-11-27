from typing import Type, Dict
from src.refacto.shared.commands.command import Command
from src.refacto.shared.handler.handler import Handler

class Mediator:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._handlers: Dict[Type[Command], Handler] = {}
            self._initialized = True


    def register_handler(self, command_type: Type[Command], handler: Handler):
        self._handlers[command_type] = handler


    def send(self, command: Command):
        command_type = type(command)
        if command_type not in self._handlers:
            raise Exception("La commande ne peut pas etre traité")
        handler = self._handlers[command_type]
        return handler.handle(command)
    