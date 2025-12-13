from os import listdir
from os.path import join
from pathlib import Path

from src.back.core.application.ports.file_factory import FileFactory
from src.back.search.application.ports.persistence.file import File
from src.back.search.infrastructure.file.json_file import JSONFile
from src.back.search.infrastructure.file.text_file import TextFile
from src.back.search.infrastructure.file.fasttext_file import FasttextFile


class FileFactory(FileFactory):

    def create_file(self, file_path: Path) -> File:
        file_path_str = str(file_path)
        if file_path_str.endswith(".json"):  return JSONFile(file_path_str)
        if file_path_str.endswith(".bin"):   return FasttextFile(file_path_str)
        return TextFile(file_path_str)
    

    def create_files_from_folder(self, folder_path: Path) -> list[File]:
        return [self.create_file(join(folder_path, filename)) for filename in sorted(listdir(folder_path))] 
