from src.back.search.shared.handler.handler import Handler
# dependencies resolver
from src.back.search.embeddings.embedding_dependency_resolver import EmbeddingDependencyResolver
from src.back.search.tf_idf.tf_idf_dependency_resolver import TfIdfDependencyResolver
# search model
from src.back.search.tf_idf.tf_idf_search_model import TFIDFSearchModel
from src.back.search.embeddings.embedding_search_model import EmbeddingSearchModel

from src.back.search.shared.commands.rich_search_command import RichSearchCommand # TODO Change that

class DependenciesHandler(Handler):

    def __init__(self):
        super().__init__()


    def handle(self, command: RichSearchCommand):
        self.resolve_dependencies(command)
        return self._next.handle(command) # TODO retirer le return

    def resolve_dependencies(self, command: RichSearchCommand):
        preprocessor = command.get_preprocessor()
        search_model = command.get_search_model()
        search_file_service = command.get_search_file_service()
        if isinstance(search_model, TFIDFSearchModel): TfIdfDependencyResolver(preprocessor, search_file_service).resolve_dependencies()
        elif isinstance(search_model, EmbeddingSearchModel): EmbeddingDependencyResolver(preprocessor, search_file_service).resolve_dependencies()
        else:
            raise ValueError("Le modèle n'est pas renconu, impossible de résoudre ses dépendances")

