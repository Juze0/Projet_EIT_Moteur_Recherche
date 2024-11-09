from abc import ABC, abstractmethod

from src.utils.result_file_ensurer import ResultFileEnsurer

class Calculator(ABC):
    """
    Classe de base pour tous les calculateurs. Implique que les classes filles 
    doivent redéfinir la méthode pour obtenir une carte de méthodes vers les fichiers.
    """
    def __init__(self, preprocessor, file_handler, class_name_to_check):
        #### -----------------------
        self.preprocessor = preprocessor
        self.preprocessor_name = preprocessor.name
        self.result_files_ensurer = ResultFileEnsurer(self.get_file_processing_map(), file_handler)
        self.result_files_ensurer.check_and_create_all(class_name_to_check, self.preprocessor_name)

    @abstractmethod
    def get_file_processing_map(self):
        """
        Doit retourner un dictionnaire associant les types de fichiers aux méthodes de traitement.
        """
        pass
