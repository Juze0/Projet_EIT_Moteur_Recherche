from src.refacto.shared.handler.handler import Handler
from src.refacto.shared.commands.command import Command
from src.refacto.shared.commands.rich_search_command import RichSearchCommand
# preprocessors
from src.preprocessing.preprocessor import Preprocessor
from src.preprocessing.nltk_preprocessor import NLTKPreprocessor
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor
# search models
from src.search_models.search_model import SearchModel
from src.search_models.we_fasttext.embedding_search_model import EmbeddingSearchModel
from src.search_models.tf_idf.tf_idf_search_model import TFIDFSearchModel

from src.refacto.shared.service.search_file_service import SearchFileService

from re import sub

class EnrichCommandHandler(Handler):

    def handle(self, command: Command):
        self._next.handle(self._enrich_command(command))


    def _enrich_command(self, command: Command) -> Command:
        cmd_search_model = command.get_search_model()
        cmd_preprocessor = command.get_preprocessor()
        search_file_service = SearchFileService(cmd_search_model, cmd_preprocessor)
        search_model = self._get_search_model(cmd_search_model, search_file_service)
        return RichSearchCommand(
            self._get_preprocessor(cmd_preprocessor),
            search_model,
            search_file_service,
            command.get_query()
        )
    

    def _remove_spaces_and_lower(self, text: str) -> str:
        return sub(r"\s+", "", text).lower()
    

    def _get_preprocessor(self, preprocessor: str) -> Preprocessor:
        preprocessor = self._remove_spaces_and_lower(preprocessor)
        if (preprocessor == "spacy"):  return SpaCyPreprocessor()
        if (preprocessor == "nltk"):  return NLTKPreprocessor()
        # TODO traiter mieux cette erreur (Le handler ne traite pas le requete et renvoi un message d'erreur à l'ui)
        raise ValueError("Le preprocesseur " + preprocessor + "n'est pas reconnu" )
    
    
    def _get_search_model(self, search_model: str, search_file_service: SearchFileService) -> SearchModel:
        search_model = self._remove_spaces_and_lower(search_model)
        if (search_model == "embedding"):  return EmbeddingSearchModel(search_file_service)
        if (search_model == "tfidf"):  return TFIDFSearchModel()
        # TODO traiter mieux cette erreur (Le handler ne traite pas le requete et renvoi un message d'erreur à l'ui)
        raise ValueError("Le modèle de recherche " + search_model + "n'est pas reconnu" )



