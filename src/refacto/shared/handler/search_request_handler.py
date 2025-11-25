from src.refacto.shared.handler.handler import Handler
from src.refacto.shared.commands.rich_search_command import RichSearchCommand
# search models
from src.search_models.we_fasttext.embedding_search_model import EmbeddingSearchModel
from src.search_models.tf_idf.tf_idf_search_model import TFIDFSearchModel
from src.search_models.we_fasttext.document_vector_calculator import DocumentVectorCalculator


class SearchRequestHandler(Handler):

    def handle(self, command: RichSearchCommand):
        return self._launch_search_request(command) # TODO à faire évoluer pour la partie évaluatioon

    def _launch_search_request(self, command: RichSearchCommand):
        preprocessed_query = self._preprocess_query(command)
        search_model = command.get_search_model()
        search_file_service = command.get_search_file_service()
        if (isinstance(search_model, EmbeddingSearchModel)):
            document_embeddings = search_file_service.get_documents_embeddings()
            return search_model.calculate_docs_to_answer_query_docs(
                preprocessed_query,
                DocumentVectorCalculator(search_file_service.get_fassttext_model()),
                document_embeddings
            )
        if (isinstance(search_model, TFIDFSearchModel)): 
            return search_model.calculate_docs_to_answer_query_docs(
                preprocessed_query,
                search_file_service.get_idf(),
                search_file_service.get_tf_idf_vectors(),
                search_file_service.get_full_vocab()
            )
        raise ValueError(f"Le modèle n'est pas reconnu !")

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

