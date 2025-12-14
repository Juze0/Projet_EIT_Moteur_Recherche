from abc import ABC, abstractmethod
from pathlib import Path

from src.back.core.application.ports.file import File


class FileFactory(ABC):

    @abstractmethod
    def get_file(self, file_path: Path) -> File:
        raise NotImplementedError("This method in not implemented !")


    @abstractmethod
    def get_files_from_folder(self, folder_path: Path) -> list[File]:
        raise NotImplementedError("This method in not implemented !")

