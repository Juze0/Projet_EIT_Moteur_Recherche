from abc import ABC, abstractmethod

from src.refacto.shared.controller import Controller

class UI(ABC):

    def __init__(self, controller: Controller):
        self._controller = controller


    @abstractmethod
    def run(self):
        raise NotImplementedError("La méthode n'est pas implémentée")


    def calculate_docs_to_answer_query_docs(self, preprocessor: str, search_model: str, query: str):
        return self._controller.calculate_docs_to_answer_query_docs(preprocessor, search_model, query)
    
    
    # TODO A rendre de nouveau fonctionnel (Donc définir une command d'évalutation)
    def start_evaluation(self):
        """Launches the evaluation process."""
        self.test_model.complete_eval()
