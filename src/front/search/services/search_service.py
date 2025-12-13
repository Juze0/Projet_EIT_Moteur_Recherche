from src.front.search.state.search_state import SearchState
from src.back.search.application.dtos.search_request_dto import SearchRequestDTO
from src.back.search.application.search_controller import SearchController

class SearchService:

    def __init__(self, controller: SearchController, state: SearchState):
        self._controller = controller
        self._state = state


    def change_preprocessor(self, preprocessor: str):
        self._state.set_preprocessor(preprocessor)


    def change_model(self, model: str):
        self._state.set_model(model)


    def search(self, query: str):
        self._state.set_last_query(query)
        return self._controller.calculate_docs_to_answer_query_docs(
            SearchRequestDTO(self._state.get_preprocessor(), self._state.get_model(), self._state.get_last_query())
        )
