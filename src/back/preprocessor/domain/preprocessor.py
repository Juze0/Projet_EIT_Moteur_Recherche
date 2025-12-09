from abc import ABC, abstractmethod

class Preprocessor(ABC):

    @abstractmethod
    def normalize(self, text: str):
        raise NotImplementedError("This method in not implemented in the subclasses !")

    @abstractmethod
    def lemmatize(self, tokens: str):
        raise NotImplementedError("This method in not implemented in the subclasses !")
    
    def normalize_then_lemmatize(self, content: str) -> str:
        return self.lemmatize(self.normalize(content))


