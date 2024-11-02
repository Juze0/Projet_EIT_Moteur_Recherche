import os
import sys
import json
from data.json_file_type import JSONFileType

class JSONFileHandler:
    """
    Classe dédiée au chargement et à la sauvegarde des données JSON.
    """
    def __init__(self):
        # Si nécessaire, vous pouvez initialiser des attributs ici.
        pass

    # ********* UTILS
    def path_exists(self, file_path):
        return os.path.exists(file_path)
    
    def get_full_path(self, json_file_type, file_name_remaining=""):
        file_name = f"{json_file_type.value}_{file_name_remaining}.json" if file_name_remaining != "" else f"{json_file_type.value}.json"
        full_file_path = os.path.join(JSONFileType.JSON_FILES_FOLDER.value, file_name)
        return full_file_path
    
    def valid_file_name(json_file_type):
        return isinstance(json_file_type, JSONFileType)
    
    # ****************** SAVE OPERATIONS
    def save_as_json_using_enum(self, data, json_file_type, file_name_remaining=""):
        """
        Sauvegarde les données sous forme de JSON dans un fichier avec un nom basé sur le type de fichier et le nom du preprocessor.
        Vérifie que le préfix du nom du fichier appartient bien à JSONFileType.
        """
        if JSONFileType.valid_file_name(json_file_type):
            self.save_as_json(data, self.get_full_path(json_file_type, file_name_remaining))

    def save_as_json(self, data, file_path):
        """
        Enregistre les données sous forme de JSON dans un fichier.
        """
        folder_path = os.path.dirname(file_path)
        if not self.path_exists(folder_path):
            print(f"[CREATION]: Dossier {folder_path} n'existe pas, création en cours...")
            os.makedirs(folder_path)  # Créer le dossier
        
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ****************** LOAD OPERATIONS
    
    def load_json_using_enum(self, json_file_type, file_name_remaining=""):
        """
        Charge le contenu d'un fichier JSON et le renvoie sous forme de dictionnaire.
        """
        file_path = self.get_full_path(json_file_type, file_name_remaining)
        return self.load_json(file_path)
    

    def load_json(self, complete_file_name):
        """
        Charge le contenu d'un fichier JSON et le renvoie sous forme de dictionnaire.
        """
        if not self.path_exists(complete_file_name):
            print(f"[ERROR]: le fichier {complete_file_name} n'existe pas.")
            sys.exit(1) 
        else:
            print(f"[READ]: {complete_file_name}")

        with open(complete_file_name, "r", encoding='utf-8') as f:
            return json.load(f)