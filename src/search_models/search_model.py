from abc import ABC, abstractmethod

class SearchModel(ABC):
    """
    Classe abstraite représentant un modèle de recherche. 
    Les sous-classes doivent implémenter les méthodes pour le prétraitement de la requête utilisateur et le calcul de la similarité.
    """

    def __init__(self, preprocessor):
        self.preprocessor = preprocessor

    @abstractmethod
    def preprocess_query(self, query):
        """Prend une requête utilisateur et effectue le prétraitement pour la transformer en liste de tokens."""
        raise NotImplementedError("This method in not implemented in the subclasses !")

    @abstractmethod
    def calculate_docs_to_answer_query_docs(self, query, top_n=10):
        """Prend une requête utilisateur et calcule la similarité cosinus entre la requête et les documents du corpus."""
        raise NotImplementedError("This method in not implemented in the subclasses !")
