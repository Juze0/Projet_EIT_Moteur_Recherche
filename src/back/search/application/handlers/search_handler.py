from typing import TypeVar, Generic

from src.back.core.application.handler import Handler
from src.back.search.application.commands.search_command import SearchCommand

from src.back.search.domain.search_model import SearchModel
from src.back.search.domain.search_requirement import SearchRequirement
from src.back.search.shared.handler.dependency_resolver import DependencyResolver

M = TypeVar("M", SearchModel)
R = TypeVar("R", SearchRequirement)
D = TypeVar("D", DependencyResolver)


class SearchHandler(Handler, Generic[M, R, D]):

    def __init__(self, search_model: M, search_requirement: R, depency_resolver: D):
        super.__init__(self)
        self.search_model = search_model
        self.search_requirement = search_requirement
        self.depency_resolver = depency_resolver


    def handle(self):
        self.depency_resolver.resolve_dependencies()
        return self.search_model.calculate_docs_to_answer_query_docs(self.search_requirement)