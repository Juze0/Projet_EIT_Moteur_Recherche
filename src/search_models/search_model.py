from abc import ABC, abstractmethod

class SearchModel(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def calculate_docs_to_answer_query_docs(self, query, top_n=10):
        """Prend une requête utilisateur et calcule la similarité cosinus entre la requête et les documents du corpus."""
        raise NotImplementedError("This method in not implemented in the subclasses !")
