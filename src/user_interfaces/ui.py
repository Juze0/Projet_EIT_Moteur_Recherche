from abc import ABC, abstractmethod

from src.refacto.front.services.search_service import SearchService

class UI(ABC):

    def __init__(self, search_service: SearchService):
        self._search_service = search_service


    @abstractmethod
    def run(self):
        raise NotImplementedError("La méthode n'est pas implémentée")
    
    
    # TODO A rendre de nouveau fonctionnel (Donc définir une command d'évalutation)
    def start_evaluation(self):
        """Launches the evaluation process."""
        self.test_model.complete_eval()
