from .command import Command
from src.back.search.shared.search_model import SearchModel
from src.back.preprocessing.preprocessor import Preprocessor


class RichSearchContextCommand(Command[Preprocessor, SearchModel]):
    
    def __init__(self, preprocessor: Preprocessor, search_model: SearchModel):
        super().__init__(preprocessor, search_model)
