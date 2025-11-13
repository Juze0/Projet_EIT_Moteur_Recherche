from .file import File

class TextFile(File):
    
    def __init__(self, file_path: str):
        super().__init__(file_path)


    def save(self, data_to_save):
        with open(self._file_path, "w", encoding='utf-8') as f:
            f.write(data_to_save)
        print(f"[SAVE]: Données sauvegardées dans {self._file_path}")


    def load(self, use_iterator=False):
        if not use_iterator:
            print(f"[READ]: Chargement du fichier {self._file_path}")
            with open(self._file_path, "r", encoding='utf-8') as f:
                return f.read()
        return self._load_using_iterator()


    def _load_using_iterator(self):
        print(f"[READ]: Lecture ligne par ligne du fichier {self._file_path}")
        with open(self._file_path, "r", encoding="utf-8") as f:
            for line in f:
                yield line
