import json

class File:

    def __init__(self, file_path: str):
        self._file_path = file_path

    def load_text_content(self) -> list[str]:
        print(f"[READ]: Chargement du fichier {self._file_path}")
        with open(self._file_path, "r", encoding='utf-8') as f:
            return f.read()


    def load_json_content(self) -> list[str]:
        print(f"[READ]: Chargement du fichier {self._file_path}")
        with open(self._file_path, "r", encoding='utf-8') as f:
            return json.load(f)
        
    def save_json(self, data):
        """
        Enregistre les données sous forme de JSON dans un fichier.
        """      
        with open(self._file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[SAVE]: Données sauvegardées dans {self._file_path}")

        
    def get_file_name(self) -> str:
        return self._file_path.split("/")[-1]