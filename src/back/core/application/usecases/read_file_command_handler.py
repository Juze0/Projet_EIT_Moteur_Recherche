from src.back.core.application.handler import Handler
from src.back.core.application.usecases.read_file_command import ReadFileCommand
from src.back.core.application.file_context_accessor_factory import FileContextAccessorFactory

class ReadFileCommandHandler(Handler):

    def __init__(self, file_context_accessor_factory: FileContextAccessorFactory):
        self._file_context_accessor_factory = file_context_accessor_factory

    def handle(self, command: ReadFileCommand):
        res = self._file_context_accessor_factory.create("tfidf", "spacy").get_corpus_subset_files(command.get_filenames())
        return {key: f.load() for key, f in res.items()}