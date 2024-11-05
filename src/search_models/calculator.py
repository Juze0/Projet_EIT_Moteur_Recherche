from abc import ABC, abstractmethod

class Calculator(ABC):
    """
    Classe de base pour tous les calculateurs. Implique que les classes filles 
    doivent redéfinir la méthode pour obtenir une carte de méthodes vers les fichiers.
    """

    @abstractmethod
    def get_file_processing_map(self):
        """
        Doit retourner un dictionnaire associant les types de fichiers aux méthodes de traitement.
        """
        pass
