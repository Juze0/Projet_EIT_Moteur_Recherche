from src.back.core.application.mediator import Mediator

from src.front.search.dtos.search_request_dto import SearchRequestDTO
from src.back.search.application.usecases.search_command import SearchCommand

class Controller:

    def __init__(self, mediator: Mediator):
        self._mediator = mediator


    def calculate_docs_to_answer_query_docs(self, search_request_dto: SearchRequestDTO):
        return self._mediator.send(SearchCommand(search_request_dto.query, 10,
                                                 search_request_dto.preprocessor,
                                                 search_request_dto.search_model))
    
