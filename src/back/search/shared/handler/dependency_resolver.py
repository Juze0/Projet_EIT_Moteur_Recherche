from src.back.search.application.commands.search_command import SearchCommand

from abc import ABC, abstractmethod

class DependencyResolver(ABC):
    
    @abstractmethod
    def resolve_dependencies(self, command: SearchCommand):
        raise NotImplementedError("This method in not implemented !")