from abc import ABC, abstractmethod

from src.back.search.application.dtos.search_request_dto import SearchRequestDTO
from src.back.search.application.dtos.search_response_dto import SearchResponseDTO

class SearchInput(ABC):

    @abstractmethod
    def search(self, dto: SearchRequestDTO) -> SearchResponseDTO:
        raise NotImplementedError("Search method is not implemented")