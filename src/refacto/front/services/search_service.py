from src.refacto.front.state.search_state import SearchState
from src.refacto.shared.controller import Controller

class SearchService:

    def __init__(self, controller: Controller, state: SearchState):
        self._controller = controller
        self._state = state


    def change_preprocessor(self, preprocessor: str):
        self._state.set_preprocessor(preprocessor)


    def change_model(self, model: str):
        self._state.set_model(model)


    def search(self, query: str):
        self._state.set_last_query(query)
        return self._controller.calculate_docs_to_answer_query_docs(
            preprocessor=self._state.get_preprocessor(),
            search_model=self._state.get_model(),
            query=self._state.get_last_query(),
        )
