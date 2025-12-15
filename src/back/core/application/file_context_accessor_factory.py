from src.back.core.application.ports.file_factory import FileFactory
from src.back.core.application.ports.paths_provider import PathsProvider
from src.back.core.application.file_context_accessor import FileContextAccessor

class FileContextAccessorFactory:

    def __init__(self, paths_provider: PathsProvider, file_factory: FileFactory):
        self._file_factory = file_factory
        self._paths_provider = paths_provider


    def create(self, search_model: str, preprocessor: str):
        return FileContextAccessor(
            paths_provider=self._paths_provider,
            file_factory=self._file_factory,
            search_model_name=search_model,
            preprocessor_name=preprocessor
        )
