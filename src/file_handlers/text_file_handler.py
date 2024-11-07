from .file_hierarchy_enum import FileHierarchyEnum
from .file_handler import FileHandler

class TextFileHandler(FileHandler):
    """
    Classe dédiée au chargement et à la sauvegarde des données texte.
    Hérite de FileHandler pour bénéficier des opérations génériques sur les fichiers.
    """

    ## SINGLETON IMPLEMENTATION
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TextFileHandler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        super().__init__(file_hierarchy_enum=FileHierarchyEnum)

    # SAVE AND LOAD METHODS TO OVERRIDE
    # Implémentation de la méthode save de FileHandler pour les fichiers texte
    def save(self, data, file_path):
        """
        Enregistre les données sous forme de texte dans un fichier.
        """    
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(data)
        print(f"[SAVE]: Données sauvegardées dans {file_path}")

    # Implémentation de la méthode load de FileHandler pour les fichiers texte
    def load(self, file_path):
        """
        Charge le contenu d'un fichier texte et le renvoie sous forme de chaîne de caractères.
        """
        if not self.path_exists(file_path):
            self.exit_with_error(f"Le fichier {file_path} n'existe pas.")
        
        print(f"[READ]: Chargement du fichier {file_path}")
        with open(file_path, "r", encoding='utf-8') as f:
            return f.read()
