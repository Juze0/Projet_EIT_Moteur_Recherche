import os
import sys
import json
from data.json_file_type import JSONFileType

class JSONHandler:
    """
    Classe dédiée au chargement et à la sauvegarde des données JSON.
    """

    # ********* UTILS
    @staticmethod
    def path_exists(file_path):
        return os.path.exists(file_path)
    
    @staticmethod
    def get_full_path(file_name_prefix, preprocessor_name=""):
        file_name = f"{file_name_prefix.value}_{preprocessor_name}.json" if preprocessor_name != "" else f"{file_name_prefix.value}.json"
        full_file_path = os.path.join(JSONFileType.FOLDER_NAME.value, file_name)
        return full_file_path
    
    @staticmethod
    def valid_file_name(file_name):
        return isinstance(file_name, JSONFileType)
    
    # ****************** SAVE OPERATIONS
    @staticmethod
    def save_as_json(data, file_name_prefix, preprocessor_name=""):
        """
        Sauvegarde les données sous forme de JSON dans un fichier avec un nom basé sur le type de fichier et le nom du preprocessor.
        Vérifie que le préfix du nom du fichier appartient bien à JSONFileType.
        """
        if JSONFileType.valid_file_name(file_name_prefix):
            JSONHandler.save_json_file_in_folder(data, JSONHandler.get_full_path(file_name_prefix, preprocessor_name))

    @staticmethod
    def save_json_file_in_folder(data, file_path):
        """
        Enregistre les données sous forme de JSON dans un fichier.
        """
        folder_path = os.path.dirname(file_path)
        if not JSONHandler.path_exists(folder_path):
            print(f"[CREATION]: Dossier {folder_path} n'existe pas, création en cours...")
            os.makedirs(folder_path)  # Créer le dossier
        
        if JSONHandler.path_exists(file_path):
            print(f"[WRITE]: {file_path}")
        else:
            print(f"[CREATION]: {file_path}")
        
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ****************** LOAD OPERATIONS
    
    @staticmethod
    def load_json(file_name_prefix, preprocessor_name=""):
        """
        Charge le contenu d'un fichier JSON et le renvoie sous forme de dictionnaire.
        """
        file_path = JSONHandler.get_full_path(file_name_prefix, preprocessor_name)

        if not JSONHandler.path_exists(file_path):
            print(f"[ERROR]: le fichier {file_path} n'existe pas.")
            sys.exit(1) 
        else:
            print(f"[READ]: {file_path}")

        with open(file_path, "r", encoding='utf-8') as f:
            return json.load(f)