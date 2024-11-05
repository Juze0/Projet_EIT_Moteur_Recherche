import json
from .file_hierarchy_enum import FileHierarchyEnum
from .file_handler import FileHandler

class JSONFileHandler(FileHandler):
    """
    Classe dédiée au chargement et à la sauvegarde des données JSON.
    Hérite de FileHandler pour bénéficier des opérations génériques sur les fichiers.
    """

    ## SINGLETON IMPLEMENTATION
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(JSONFileHandler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        super().__init__(file_hierarchy_enum=FileHierarchyEnum)

    # SAVE AND LOAD METHODS TO OVERRIDE
    # Implémentation de la méthode save de FileHandler pour JSON
    def save(self, data, file_path):
        """
        Enregistre les données sous forme de JSON dans un fichier.
        """
        self.create_all_missing_folders(file_path)
        
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[SAVE]: Données sauvegardées dans {file_path}")

    # Implémentation de la méthode load de FileHandler pour JSON
    def load(self, file_path):
        """
        Charge le contenu d'un fichier JSON et le renvoie sous forme de dictionnaire.
        """
        if not self.path_exists(file_path):
            self.exit_with_error(f"Le fichier {file_path} n'existe pas.")
        
        print(f"[READ]: Chargement du fichier {file_path}")
        with open(file_path, "r", encoding='utf-8') as f:
            return json.load(f)
