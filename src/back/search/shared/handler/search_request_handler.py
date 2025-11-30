from src.back.search.shared.handler.handler import Handler
from src.back.search.shared.commands.rich_search_command import RichSearchCommand
# search models
from src.back.search.embeddings.embedding_search_model import EmbeddingSearchModel
from src.back.search.tf_idf.tf_idf_search_model import TFIDFSearchModel
from src.back.search.embeddings.calculators.document_vector_calculator import DocumentVectorCalculator
# search requirements
from src.back.search.tf_idf.tf_idf_search_requirement import TfIdfSearchRequirement
from src.back.search.embeddings.embedding_search_requirement import EmbeddingSearchRequirement


class SearchRequestHandler(Handler):

    def handle(self, command: RichSearchCommand):
        return self._launch_search_request(command) # TODO à faire évoluer pour la partie évaluatioon

    def _launch_search_request(self, command: RichSearchCommand):
        preprocessed_query = self._preprocess_query(command)
        search_model = command.get_search_model()
        search_file_service = command.get_search_file_service()
        requirement = None
        if (isinstance(search_model, EmbeddingSearchModel)):
            requirement = EmbeddingSearchRequirement(
                preprocessed_query,
                10,
                DocumentVectorCalculator(search_file_service.get_fassttext_model()),
                search_file_service.get_documents_embeddings()
            )
        elif (isinstance(search_model, TFIDFSearchModel)):
            requirement = TfIdfSearchRequirement(
                preprocessed_query,
                10,
                search_file_service.get_idf(),
                search_file_service.get_tf_idf_vectors(),
                search_file_service.get_full_vocab()
            )
        if requirement == None:
            raise ValueError(f"Le modèle n'est pas reconnu !")
        return search_model.calculate_docs_to_answer_query_docs(requirement)

    def _preprocess_query(self, command: RichSearchCommand) -> str:
        query = command.get_query()
        preprocessor = command.get_preprocessor()
        search_model = command.get_search_model()
        if (isinstance(search_model, EmbeddingSearchModel)): 
            return preprocessor.normalize_text(query)
        if (isinstance(search_model, TFIDFSearchModel)): 
            return preprocessor.normalize_and_lemmatize(query)

    def _handle_embedding_search_request(self, model: EmbeddingSearchModel):
        return model.calculate_docs_to_answer_query_docs()

