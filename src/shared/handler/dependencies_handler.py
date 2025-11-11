import time
from src.shared.handler.base_handler import BaseHandler
from src.shared.files.file import File
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum

from os import makedirs, remove, listdir
from os.path import exists, join, dirname, getsize
from sys import exit

class DependenciesHandler(BaseHandler):

    def __init__(self):
        super().__init__()
    
    
    def if_file_not_found_launch_calculation(self, file: File, calculation_func, *args, **kwargs):
        if file.exists():
            print(f"[INFO] Le fichier {file.get_file_name()} est disponible ! Voici son chemin {file.get_path()}")
            return
        print("-----------------")
        print(f"[CREATION START] Le fichier {file.get_path()} n'existe pas, création en cours...")
        file.create_all_missing_folders()
        start_time = time.time()
        data_to_save = calculation_func(*args, **kwargs)
        end_time = time.time()
        print(f"[CREATION END] La création du fichier {file.get_file_name()} s'est terminée en {self.get_creation_duration_time(start_time, end_time)}!")
        if data_to_save is None:
            # TODO changer ce comportement là, la sauvegarde est forcément réaliser par un DependencieHandler
            print(f"[INFO] La sauvegarde du fichier a été déléguée au fichier de calcul correspondant")
        else:
            file.save_json(data_to_save) # TODO, On addresse désormais ce problème
        print("-----------------")


    # Récupérer depuis file_handler
    def get_full_path_files_of_folder(self, folder_name: str) -> list[str]:
        return [join(folder_name, filename) for filename in listdir(folder_name)]
    
    def get_file_path(self, filename_enum, filename_suffix=""):
        """Utilise l'enum décrivant la hierarchie de fichier pour obtenir le chemin du fichier spéicifié !"""
        return FileHierarchyEnum.get_file_path(filename_enum, filename_suffix)