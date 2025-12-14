from abc import ABC, abstractmethod

class File(ABC):

    @abstractmethod
    def load(self, use_iterator=False):
        raise NotImplementedError("This method in not implemented !")
    
    @abstractmethod
    def save(self, data_to_save):
        raise NotImplementedError("This method in not implemented !")

