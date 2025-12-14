from src.front.search.state.search_state import SearchState
from src.back.search.application.dtos.search_request_dto import SearchRequestDTO
from src.back.search.application.ports.input.search_input import SearchInput

class SearchService:

    def __init__(self, search_input: SearchInput, state: SearchState):
        self._search_input = search_input
        self._state = state


    def change_preprocessor(self, preprocessor: str):
        self._state.set_preprocessor(preprocessor)


    def change_model(self, model: str):
        self._state.set_model(model)


    def search(self, query: str):
        self._state.set_last_query(query)
        return self._search_input.search(
            SearchRequestDTO(preprocessor=self._state.get_preprocessor(),
                             search_model=self._state.get_model(),
                             query=self._state.get_last_query(),
                             top_n=15))
