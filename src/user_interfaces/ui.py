from abc import ABC, abstractmethod

from src.refacto.front.services.search_ui_service import SearchUiService

class UI(ABC):

    def __init__(self, search_ui_service: SearchUiService):
        self._search_ui_service = search_ui_service


    @abstractmethod
    def run(self):
        raise NotImplementedError("La méthode n'est pas implémentée")
    
    
    # TODO A rendre de nouveau fonctionnel (Donc définir une command d'évalutation)
    def start_evaluation(self):
        """Launches the evaluation process."""
        self.test_model.complete_eval()
