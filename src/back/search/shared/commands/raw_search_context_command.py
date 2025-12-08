from ...application.commands.search_command import SearchCommand

class RawSearchContextCommand(SearchCommand[str, str]):
    
    def __init__(self, preprocessor: str, search_model: str):
        super().__init__(preprocessor, search_model)
