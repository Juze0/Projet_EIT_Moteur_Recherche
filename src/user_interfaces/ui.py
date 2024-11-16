from abc import ABC, abstractmethod

from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum

from src.preprocessing.nltk_preprocessor import NLTKPreprocessor
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor

from src.search_models.tf_idf.tf_idf_search_model import TFIDFSearchModel
from src.search_models.we_fasttext.embedding_search_model import EmbeddingSearchModel

from src.evaluation.test import Test
from src.evaluation.result_test_reader import ResultTestReader


class UI(ABC):
    """Interface for user interaction classes."""

    def __init__(self):
        print("Par défaut, vous utilisez le modèle TF-IDF et le preprocessor Spacy")
        self.preprocessor = SpaCyPreprocessor()
        self.model = TFIDFSearchModel(self.preprocessor)
        self.test_model = Test(self.model)
        self.result_test_reader = ResultTestReader(FileHierarchyEnum.get_file_path(FileHierarchyEnum.EVAL_TFIDF))


    ######## Setters
    def set_preprocessor(self, preprocessor):
        """Change le préprocesseur et crée un nouveau modèle associé à ce préprocesseur."""
        self.preprocessor = preprocessor
        self.set_model(self.model.__class__)  # Crée un nouveau modèle du même type, mais avec le nouveau préprocesseur.


    def set_model(self, model_class):
        """Met à jour le modèle en fonction de la classe du modèle et du préprocesseur actuel."""
        if model_class == TFIDFSearchModel:
            self.model = TFIDFSearchModel(self.preprocessor)  # Crée un modèle TF-IDF avec le préprocesseur actuel
            self.result_test_reader.set_file_path(FileHierarchyEnum.get_file_path(FileHierarchyEnum.EVAL_TFIDF))
        elif model_class == EmbeddingSearchModel:
            self.model = EmbeddingSearchModel(self.preprocessor)  # Crée un modèle Embedding avec le préprocesseur actuel
            self.result_test_reader.set_file_path(FileHierarchyEnum.get_file_path(FileHierarchyEnum.EVAL_EMBEDDINGS))
        else:
            raise ValueError(f"Modèle {model_class} non pris en charge.")
        self.test_model.set_model_to_test(self.model)


    def calculate_docs_to_answer_query_docs(self, query):
        # Obtenir tous les résultats du modèle
        all_results = self.model.calculate_docs_to_answer_query_docs(query)
        top_10_results = dict(list(all_results.items())[:10])
        return top_10_results
    

    def start_evaluation(self):
        """Launches the evaluation process."""
        self.test_model.complete_eval()

    ######## A redéfinir dans les classes filles !

    @abstractmethod
    def run(self):
        """Runs the CLI interface."""
        pass