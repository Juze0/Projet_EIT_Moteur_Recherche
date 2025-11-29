from .command import Command

class RawSearchContextCommand(Command[str, str]):
    
    def __init__(self, preprocessor: str, search_model: str):
        super().__init__(preprocessor, search_model)
