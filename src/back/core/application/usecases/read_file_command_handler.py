from src.back.core.application.handler import Handler
from src.back.core.application.usecases.read_file_command import ReadFileCommand
from src.back.core.application.file_context_accessor import FileContextAccessor

class ReadFileCommandHandler(Handler):

    def __init__(self, file_retriever_service: FileContextAccessor):
        self._file_retriever_service = file_retriever_service

    def handle(self, command: ReadFileCommand):
        return self._file_retriever_service.get_corpus_subset_files(command.get_filenames())