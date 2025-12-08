from abc import ABC, abstractmethod
from src.back.search.domain.search_model_dependency import SearchModelDependency
from src.back.search.domain.search_query import SearchQuery

class SearchModel(ABC):

    def __init__(self, model_dependency: SearchModelDependency):
        self._model_dependency = model_dependency


    @abstractmethod
    def calculate_docs_to_answer_query_docs(self, search_query: SearchQuery):
        raise NotImplementedError("This method in not implemented in the subclasses !")
