from abc import ABC, abstractmethod

class DependencyResolver(ABC):
    
    @abstractmethod
    def resolve_dependencies(self):
        raise NotImplementedError("This method in not implemented !")