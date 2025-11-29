from .command import Command
from src.search_models.search_model import SearchModel
from src.preprocessing.preprocessor import Preprocessor


class RichSearchContextCommand(Command[Preprocessor, SearchModel]):
    
    def __init__(self, preprocessor: Preprocessor, search_model: SearchModel):
        super().__init__(preprocessor, search_model)
