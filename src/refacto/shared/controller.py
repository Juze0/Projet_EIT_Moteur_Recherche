from src.refacto.shared.mediator import Mediator
# command
from src.refacto.shared.commands.raw_search_command import RawSearchCommand

class Controller:

    def __init__(self, mediator: Mediator):
        self._mediator = mediator


    def calculate_docs_to_answer_query_docs(self, preprocessor: str, search_model: str, query: str):
        return self._mediator.send(RawSearchCommand(preprocessor, search_model, query))
    
