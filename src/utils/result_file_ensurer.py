import time
from src.file_handlers.file_compressor_decorator import FileCompressorDecorator

class ResultFileEnsurer():

    def __init__(self, files_map, file_handler):
        " Initialise RequiredFileChecker avec un dictionnaire mappant chaque nom de fichier à sa méthode de calcul correspondante."
        super().__init__()
        self.files_map = files_map
        self.file_handler = file_handler

    # SAVE & LOAD OPERATIONS
    # Allow ResultFileEnsurer to use FileHandler's methods

    def save(self, data, file_path):
        self.file_handler.save(data, file_path)

    def load_using_enum(self, filename_enum, file_name_suffix=""):
        return self.file_handler.load_using_enum(filename_enum, file_name_suffix)

    #setter
    def set_file_handler(self, new_file_handler):
        self.file_handler = new_file_handler

    # Specific methods to ResultFileEnsurer, here, we want to ensure all required files are there. if no, we create them !

    def check_and_create_all(self, class_name_to_check, filename_suffix=""):
        " Vérifie et crée tous les fichiers manquants en fonction de `files_map`."
        print(f"#####  Vérification des prérequis pour utiliser {class_name_to_check}")
        for filename_enum, calculation_method in self.files_map.items():
            complete_file_path = self.file_handler.get_file_path(filename_enum, filename_suffix)
            self.check_and_create(complete_file_path, calculation_method)
        print()

    def check_and_create(self, complete_file_path, calculation_method):
        " Vérifie l'existence du fichier et le crée si nécessaire."
        if self.file_handler.path_exists(complete_file_path):
            print(f"[INFO] Le fichier {complete_file_path} est disponible !")
            return
        if self.file_handler.path_exists(f"{complete_file_path}.xz"): # Le fichier existe au format compréssé !
            print(f"[INFO] Le fichier {complete_file_path} est disponible au format compréssé. Lancement de la décompression !")
            FileCompressorDecorator(self.file_handler).load(complete_file_path)
            return
        self.create_missing_file(complete_file_path, calculation_method)

    def create_missing_file(self, complete_file_path, calculation_method):
        "Crée le fichier manquant en mesurant le temps de création."
        print("-----------------")
        print(f"[INFO] Le fichier {complete_file_path} n'existe pas, création en cours...")
        start_time = time.time()
        self.save(calculation_method(), complete_file_path)
        end_time = time.time()
        creation_time = end_time - start_time
        print(f"[INFO] La création du fichier {complete_file_path} s'est terminée en  {self.get_creation_duration_time(creation_time)}!")
        print("-----------------")

    def get_creation_duration_time(self, creation_time):
        if creation_time < 60:
            return f"{creation_time:.4f} seconds"
        creation_time_minutes = creation_time / 60
        return f"{creation_time_minutes:.2f} minutes"
