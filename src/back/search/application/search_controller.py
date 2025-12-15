from src.back.core.application.mediator import Mediator
from src.back.search.application.ports.input.search_input import SearchInput
from src.back.search.application.dtos.search_request_dto import SearchRequestDTO
from src.back.search.application.usecases.search_command import SearchCommand
from src.back.core.application.usecases.read_file_command import ReadFileCommand
from src.back.search.application.dtos.search_response_dto import SearchResponseDTO, SearchResultDTO

class SearchController(SearchInput):

    def __init__(self, mediator: Mediator):
        self._mediator = mediator


    def search(self, search_request_dto: SearchRequestDTO):
        res = self._mediator.send(SearchCommand(query=search_request_dto.query,
                                                 top_n=search_request_dto.top_n,
                                                 preprocessor=search_request_dto.preprocessor,
                                                 search_model=search_request_dto.search_model))
        doc_content_map = self._mediator.send(ReadFileCommand([result.document_name for result in res ]))
        results = [ 
            SearchResultDTO(document_name=result.document_name,
                            score=result.score,
                            content=doc_content_map[result.document_name]) 
            for result in res ]
        return SearchResponseDTO( query=search_request_dto.query, results=results)
        
    
