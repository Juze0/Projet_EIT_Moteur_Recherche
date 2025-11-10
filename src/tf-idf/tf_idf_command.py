from src.shared.command import Command

class TfIdfCommand(Command):

    def __init__(self, model, preprocessor, query):
        super().__init__(model, preprocessor, query)