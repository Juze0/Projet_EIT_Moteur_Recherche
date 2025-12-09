from ...application.commands.search_command import SearchCommand
from src.back.search.domain.search_model import SearchModel
from src.back.preprocessor.domain.preprocessor import Preprocessor


class RichSearchContextCommand(SearchCommand[Preprocessor, SearchModel]):
    
    def __init__(self, preprocessor: Preprocessor, search_model: SearchModel):
        super().__init__(preprocessor, search_model)
