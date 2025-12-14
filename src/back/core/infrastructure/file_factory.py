from os import listdir
from os.path import join
from pathlib import Path

from src.back.core.application.ports.file_factory import FileFactory
from src.back.core.application.ports.file import File
from src.back.core.infrastructure.persistence.json_file import JSONFile
from src.back.core.infrastructure.persistence.text_file import TextFile
from src.back.core.infrastructure.persistence.fasttext_file import FasttextFile


class FileFactory(FileFactory):

    def get_file(self, file_path: Path) -> File:
        file_path_str = str(file_path)
        if file_path_str.endswith(".json"):  return JSONFile(file_path_str)
        if file_path_str.endswith(".bin"):   return FasttextFile(file_path_str)
        return TextFile(file_path_str)
    

    def get_files_from_folder(self, folder_path: Path) -> list[File]:
        return [self.get_file(join(folder_path, filename)) for filename in sorted(listdir(folder_path))] 
