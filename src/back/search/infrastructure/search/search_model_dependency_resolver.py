from src.back.preprocessor.domain.preprocessor import Preprocessor
from src.back.search.shared.service.search_file_service import SearchFileService
from src.back.search.application.ports.search.dependency_resolver import DependencyResolver
from src.back.search.application.ports.persistence.file import File

class SearchModelDependencyResolver(DependencyResolver):

    def __init__(self, preprocessor: Preprocessor, search_file_service: SearchFileService):
        self._preprocessor = preprocessor
        self._search_file_service = search_file_service

    def if_file_not_found_launch_calculation(self, file: File, calculation_func, *args, **kwargs):
        if file.exists():
            print(f"[INFO] Le fichier {file.get_file_name()} est disponible ! Voici son chemin {file.get_path()}")
            return
        print("-----------------")
        print(f"[CREATION START] Le fichier {file.get_path()} n'existe pas, création en cours...")
        file.create_all_missing_folders() # TODO, délégué cette méthode 
        data_to_save = calculation_func(*args, **kwargs)
        if data_to_save is None:
            # TODO changer ce comportement là, la sauvegarde est forcément réaliser par un DependencieHandler
            print(f"[INFO] La sauvegarde du fichier a été déléguée au fichier de calcul correspondant")
        else:
            file.save(data_to_save) # TODO, On addresse désormais ce problème
        print("-----------------")