import fasttext

from .file import File

class FasttextFile(File):
    
    def __init__(self, file_path: str):
        super().__init__(file_path)


    def save(self, data_to_save):
        data_to_save.save_model(self._file_path)
        print(f"[SAVE] Le modèle fasttext a été sauvegardé dans {self._file_path}")


    def load(self, use_iterator=False):
        print(f"[READ]: Chargement du modèle fasttext {self._file_path}")
        return fasttext.load_model(self._file_path)
   
