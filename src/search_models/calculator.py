from abc import ABC

class Calculator(ABC):
    """
    Classe de base pour tous les calculateurs. Implique que les classes filles 
    doivent redéfinir la méthode pour obtenir une carte de méthodes vers les fichiers.
    """
    def __init__(self, preprocessor):
        self.preprocessor = preprocessor