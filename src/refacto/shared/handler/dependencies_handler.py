from src.refacto.shared.handler.handler import Handler
from src.file_handlers.file import File
from src.refacto.shared.commands.command import Command

from abc import abstractmethod

from os import listdir
from os.path import join

class DependenciesHandler(Handler):

    def __init__(self):
        super().__init__()


    def handle(self, command: Command):
        command.get_dependencies_handler().resolve_dependencies(command)
        self._next.handle(command)
    
    #@abstractmethod TODO remettre
    def resolve_dependencies(self, command: Command):
        raise NotImplementedError("This method in not implemented !")