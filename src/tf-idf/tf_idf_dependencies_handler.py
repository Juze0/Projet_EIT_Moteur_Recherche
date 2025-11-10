from src.shared.handler.base_handler import BaseHandler
from src.shared.command import Command

class TfIdfDependenciesHandler(BaseHandler):

    def __init__(self):
        super().__init__()

    def handle(self, command: Command):
        raise NotImplementedError("This method in not implemented in the current class !")