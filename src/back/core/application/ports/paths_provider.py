from abc import ABC, abstractmethod
from pathlib import Path


class PathsProvider(ABC):

    @abstractmethod
    def wiki_corpus_dir(self) -> Path:
        raise NotImplementedError("This method in not implemented !")

    @abstractmethod
    def correction_dir(self) -> Path:
        raise NotImplementedError("This method in not implemented !")
    
    @abstractmethod
    def output_dir(self) -> Path:
        raise NotImplementedError("This method in not implemented !") 