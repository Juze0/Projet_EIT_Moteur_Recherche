from src.back.core.application.mediator import Mediator
from src.back.search.application.ports.input.search_input import SearchInput
from src.back.search.application.dtos.search_request_dto import SearchRequestDTO
from src.back.search.application.usecases.search_command import SearchCommand

class SearchController(SearchInput):

    def __init__(self, mediator: Mediator):
        self._mediator = mediator


    def search(self, search_request_dto: SearchRequestDTO):
        return self._mediator.send(SearchCommand(search_request_dto.query, 10,
                                                 search_request_dto.preprocessor,
                                                 search_request_dto.search_model))
    
