import json
from .file import File

class JSONFile(File):
    
    def __init__(self, file_path: str):
        super().__init__(file_path)


    def save(self, data_to_save):
        with open(self._file_path, "w", encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        print(f"[SAVE]: Données sauvegardées dans {self._file_path}")


    def load(self, use_iterator=False):       
        print(f"[READ]: Chargement du fichier {self._file_path}")
        with open(self._file_path, "r", encoding='utf-8') as f:
            return json.load(f)
