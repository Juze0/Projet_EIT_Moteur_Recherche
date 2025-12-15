from src.back.search.domain.search_model_name import SearchModelName
from src.back.core.application.file_context_accessor import FileContextAccessor
## command/handler
from src.back.search.application.usecases.search_command import SearchCommand
from src.back.preprocessor.domain.preprocessor_name import PreprocessorName
from src.back.preprocessor.infrastructure.preprocessor_factory import PreprocessorFactory

from src.back.core.application.ports.file_factory import FileFactory
from src.back.core.application.ports.paths_provider import PathsProvider

class SearchExecutionContextFactory:

    def __init__(self, paths_provider: PathsProvider, file_factory: FileFactory, preprocessor_factory: PreprocessorFactory):
        self._file_factory = file_factory
        self._paths_provider = paths_provider
        self._preprocessor_factory = preprocessor_factory

    def create(self, command: SearchCommand) -> SearchExecutionContext:
        preprocessor_name = PreprocessorName(command.get_preprocessor())
        model_name = SearchModelName(command.get_search_model())

        preprocessor = self._preprocessor_factory.get_preprocessor(preprocessor_name)

        search_file_service = FileContextAccessor(
            self._file_factory,
            self._paths_provider,
            model_name.value,
            preprocessor_name.value
        )

        return SearchExecutionContext(
            search_file_service=search_file_service,
            preprocessor=preprocessor,
            model_name=model_name
        )
