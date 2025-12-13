from abc import ABC, abstractmethod
from pathlib import Path

from src.back.search.application.ports.output.persistence.file import File


class FileFactory(ABC):

    @abstractmethod
    def create_file(self, file_path: Path) -> File:
        raise NotImplementedError("This method in not implemented !")


    @abstractmethod
    def create_files_from_folder(self, folder_path: Path) -> list[File]:
        raise NotImplementedError("This method in not implemented !")

