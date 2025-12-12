from typing import TypeVar, Generic

from src.back.core.application.handler import Handler
from src.back.search.application.usecases.search_command import SearchCommand

from src.back.search.domain.search_query import SearchQuery
from src.back.search.domain.search_model import SearchModel
from src.back.search.application.ports.dependency_resolver import DependencyResolver

M = TypeVar("M", bound=SearchModel)
R = TypeVar("R", bound=DependencyResolver)


class SearchHandler(Handler, Generic[M, R]):

    def __init__(self, search_model: M, dependency_resolver: R):
        super().__init__()
        self.search_model = search_model
        self.dependency_resolver = dependency_resolver


    def handle(self, command: SearchCommand):
        self.dependency_resolver.resolve_dependencies()
        return self.search_model.calculate_docs_to_answer_query_docs(SearchQuery(
            query=command.get_query(),
            top_n=command.get_top_n()
        ))