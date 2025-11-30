from abc import ABC, abstractmethod
from src.back.search.shared.search_requirement.search_requirement import SearchRequirement

class SearchModel(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def calculate_docs_to_answer_query_docs(self, search_requirement: SearchRequirement):
        """Prend une requête utilisateur et calcule la similarité cosinus entre la requête et les documents du corpus."""
        raise NotImplementedError("This method in not implemented in the subclasses !")
