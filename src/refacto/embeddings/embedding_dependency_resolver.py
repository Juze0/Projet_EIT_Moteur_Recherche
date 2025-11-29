from src.refacto.shared.handler.search_model_dependency_resolver import SearchModelDependencyResolver
from src.preprocessing.preprocessor import Preprocessor
from src.refacto.shared.service.search_file_service import SearchFileService
from src.search_models.we_fasttext.we_calculator import WECalculator
from src.search_models.we_fasttext.document_vector_calculator import DocumentVectorCalculator

class EmbeddingDependencyResolver(SearchModelDependencyResolver):

    def __init__(self, preprocessor: Preprocessor, search_file_service: SearchFileService):
        super().__init__(preprocessor, search_file_service)


    def resolve_dependencies(self):
        self.resolve_preprocessed_merged_corpus_and_model_training()
        self.resolve_documents_embeddings()


    def resolve_preprocessed_merged_corpus_and_model_training(self):
        """Retourne une carte associant les types de fichiers aux méthodes de traitement."""
        print(f"\n#####  Vérification des prérequis pour utiliser les word embeddings")
        we_calculator = WECalculator("skipgram")

        corpus_files = self._search_file_service.get_corpus_files()
        preprocessed_merged_corpus_file = self._search_file_service.get_preprocessed_corpus()
        fasttext_model = self._search_file_service.get_fassttext_model()

        self.if_file_not_found_launch_calculation(preprocessed_merged_corpus_file, we_calculator.build_normalized_corpus, self._preprocessor, corpus_files)
        self.if_file_not_found_launch_calculation(fasttext_model, we_calculator.train_model, preprocessed_merged_corpus_file)
    

    def resolve_documents_embeddings(self):
        print(f"\n#####  Vérification des prérequis pour utiliser les embeddings de chaque document du corpus !")
        fasttext_model = self._search_file_service.get_fassttext_model()
        document_vector_calculator = DocumentVectorCalculator(fasttext_model)

        corpus_files = self._search_file_service.get_corpus_files()
        preprocessed_merged_corpus_file = self._search_file_service.get_preprocessed_corpus()
        doc_embeddings = self._search_file_service.get_documents_embeddings()


        self.if_file_not_found_launch_calculation(doc_embeddings,
                                                  document_vector_calculator.calculate_embeddings_for_all_documents,
                                                  preprocessed_merged_corpus_file, [f.get_file_name() for f in corpus_files])
        print()