from src.back.core.application.handler import Handler
from src.back.core.application.usecases.read_file_command import ReadFileCommand
from src.back.core.application.search_model_file_service import SearchModelFileService

class ReadFileCommandHandler(Handler):

    def __init__(self, file_retriever_service: SearchModelFileService):
        self._file_retriever_service = file_retriever_service

    def handle(self, command: ReadFileCommand):
        return self._file_retriever_service.get_corpus_subset_files(command.get_filenames())