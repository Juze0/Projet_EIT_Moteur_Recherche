from abc import ABC, abstractmethod

class DependencyResolver(ABC): # TODO statuer sur le placement de cette classe
    
    @abstractmethod
    def resolve_dependencies(self):
        raise NotImplementedError("This method in not implemented !")