from abc import ABC, abstractmethod
from re import compile, UNICODE

class Preprocessor(ABC):
    
    """
    Abstract class for preprocessing using libraries like NLTK or Spacy.
    """

    def __init__(self, name):
        self.__name = name
        self.regex = compile(r"^[\wÀ-ÿ]+$", UNICODE) # Regex pour les mots français avec caractères spéciaux

    @abstractmethod
    def normalize_text(self, text):
        raise NotImplementedError("This method in not implemented in the subclasses !")

    @abstractmethod
    def normalize_document(self, file):
        raise NotImplementedError("This method in not implemented in the subclasses !")

    @abstractmethod
    def lemmatize(self, tokens):
        raise NotImplementedError("This method in not implemented in the subclasses !")
    
    @property
    def name(self):
        return self.__name

