from src.refacto.shared.commands.command import Command
from src.refacto.shared.handler.handler import Handler

class Mediator:

    def __init__(self):
        self._handlers: dict[Command, Handler] = {}


    def register_handler(self, command: Command, handler: Handler):
        self._handlers[command] = handler


    def send(self, command: Command):
        command_type = type(command)
        if command_type not in self._handlers:
            raise Exception("La commande ne peut pas etre traité")
        handler = self._handlers[command_type]
        return handler.handle(command)
    