from os import makedirs, remove, listdir
from os.path import exists, join, dirname, getsize
from sys import exit

from src.back.core.application.ports.file import File

class BaseFile(File):

    def __init__(self, file_path: str):
        self._file_path = file_path

    def get_path(self) -> str:
        return self._file_path
    
    def get_file_name(self) -> str:
        return self._file_path.split("/")[-1]

    def exists(self) -> bool:
        return exists(self._file_path)
    
    def get_directory(self, file_or_folder_path: str) -> str:
        return dirname(file_or_folder_path)

    def create_all_missing_folders(self):
        makedirs(self.get_directory(self._file_path), exist_ok=True)

    def join(self, *paths):
        return join(*paths)

    def exit_with_error(self, message: str):
        print(f"[ERROR]: {message}")
        exit(1)

    #TODO revoit la doc de ces deux méthodes
    def path_getsize(self, file_path: str):
        return getsize(file_path)
    
    def remove_path(self, file_path: str):
        remove(file_path)

    def get_full_path_files_of_folder(self, folder_name: str) -> list[str]:
        return [self.join(folder_name, filename) for filename in listdir(folder_name)]

