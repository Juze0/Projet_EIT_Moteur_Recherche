import time
from data.json_file_handler import JSONFileHandler

class ResultFileEnsurer(JSONFileHandler):

    def __init__(self, files_map):
        " Initialise RequiredFileChecker avec un dictionnaire mappant chaque nom de fichier à sa méthode de calcul correspondante."
        super().__init__()
        self.files_map = files_map


    def check_and_create_all(self, class_name_to_check, remaining_file_name):
        " Vérifie et crée tous les fichiers manquants en fonction de `files_map`."
        print(f"#####  Vérification des prérequis pour utiliser {class_name_to_check}")
        for file_name, calculation_method in self.files_map.items():
            complete_file_name = self.get_full_path(file_name, remaining_file_name)
            self.check_and_create(complete_file_name, calculation_method)
        print()


    def check_and_create(self, complete_file_name, calculation_method):
        " Vérifie l'existence du fichier et le crée si nécessaire."
        if self.path_exists(complete_file_name):
            print(f"[INFO] Le fichier {complete_file_name} est disponible !")
            return
        self.create_missing_file(complete_file_name, calculation_method)


    def create_missing_file(self, complete_file_name, calculation_method):
        "Crée le fichier manquant en mesurant le temps de création."
        print("-----------------")
        print(f"[INFO] Le fichier {complete_file_name} n'existe pas, création en cours...")
        start_time = time.time()
        self.save_as_json(calculation_method(), complete_file_name)
        end_time = time.time()
        creation_time = end_time - start_time
        print(f"[INFO] La création du fichier {complete_file_name} s'est terminée en  {self.get_creation_duration_time(creation_time)}!")
        print("-----------------")



    def get_creation_duration_time(self, creation_time):
        if creation_time < 60:
            return f"{creation_time:.4f} seconds"
        creation_time_minutes = creation_time / 60
        return f"{creation_time_minutes:.2f} minutes"
