from src.back.search.shared.commands.command import Command

from abc import ABC, abstractmethod

class DependencyResolver(ABC):
    
    @abstractmethod
    def resolve_dependencies(self, command: Command):
        raise NotImplementedError("This method in not implemented !")