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
    def get_filename_and_calculation_method(self, filename_enum, calculation_info, filename_suffix):
        """Pour chaque clé du dictionnaire, deux formats sont autorisés
        * 1er format:  FileHierarchyEnum.ENUM_CHOICE: calculation_method,
        * 2eme format: FileHierarchyEnum.ENUM_CHOICE: (calculation_method, extra_information_about_filename)
        Cette méthode s'occupe de la disjonction des cas !
        """
        if isinstance(calculation_info, tuple):
            calculation_method, extra_info = calculation_info
            complete_file_path = self.file_handler.get_file_path(filename_enum, f"{filename_suffix}_{extra_info}")
        else:
            calculation_method = calculation_info
            complete_file_path = self.file_handler.get_file_path(filename_enum, filename_suffix)
        return complete_file_path, calculation_method

    def check_and_create_all(self, class_name_to_check, filename_suffix=""):
        " Vérifie et crée tous les fichiers manquants en fonction de `files_map`."
        print(f"\n#####  Vérification des prérequis pour utiliser {class_name_to_check}")
        for filename_enum, calculation_info in self.files_map.items():
            complete_file_path, calculation_method = self.get_filename_and_calculation_method(filename_enum, calculation_info, filename_suffix)
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
        print(f"[CREATION START] Le fichier {complete_file_path} n'existe pas, création en cours...")
        self.file_handler.create_all_missing_folders(complete_file_path)
        start_time = time.time()
        data = calculation_method()
        if data is None:
            print(f"[INFO] La sauvegarde du fichier a été déléguée au fichier de calcul correspondant")
        else:
            self.save(data, complete_file_path)
        end_time = time.time()
        print(f"[CREATION END] La création du fichier s'est terminée en {self.get_creation_duration_time(start_time, end_time)}!")
        print("-----------------")

    def get_creation_duration_time(self, start_time, end_time):
        creation_time = end_time - start_time
        if creation_time < 60:
            return f"{creation_time:.4f} seconds"
        creation_time_minutes = creation_time / 60
        return f"{creation_time_minutes:.2f} minutes"
