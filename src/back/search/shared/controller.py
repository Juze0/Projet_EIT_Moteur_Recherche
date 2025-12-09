from src.back.core.application.mediator import Mediator
# dto
from src.front.search.dtos.search_request_dto import SearchRequestDTO
# command
from src.back.search.shared.commands.raw_search_command import RawSearchCommand

class Controller:

    def __init__(self, mediator: Mediator):
        self._mediator = mediator


    def calculate_docs_to_answer_query_docs(self, search_request_dto: SearchRequestDTO):
        return self._mediator.send(RawSearchCommand(search_request_dto.preprocessor, search_request_dto.search_model, search_request_dto.query))
    
