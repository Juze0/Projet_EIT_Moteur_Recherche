from abc import ABC, abstractmethod

from src.preprocessing.nltk_preprocessor import NLTKPreprocessor
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor

from src.search_models.tf_idf.tf_idf_search_model import TFIDFSearchModel
from src.search_models.we_fasttext.embedding_search_model import EmbeddingSearchModel

class UI(ABC):
    """Interface for user interaction classes."""

    def __init__(self):
        print("Par défaut, vous utilisez le modèle TF-IDF et le preprocessor Spacy")
        self.preprocessor = SpaCyPreprocessor()
        self.model = TFIDFSearchModel(self.preprocessor)

    ######## Setters
    def set_preprocessor(self, preprocessor):
        """Change le préprocesseur et crée un nouveau modèle associé à ce préprocesseur."""
        self.preprocessor = preprocessor
        self.set_model(self.model.__class__)  # Crée un nouveau modèle du même type, mais avec le nouveau préprocesseur.


    def set_model(self, model_class):
        """Met à jour le modèle en fonction de la classe du modèle et du préprocesseur actuel."""
        if model_class == TFIDFSearchModel:
            self.model = TFIDFSearchModel(self.preprocessor)  # Crée un modèle TF-IDF avec le préprocesseur actuel
        elif model_class == EmbeddingSearchModel:
            self.model = EmbeddingSearchModel(self.preprocessor)  # Crée un modèle Embedding avec le préprocesseur actuel
        else:
            raise ValueError(f"Modèle {model_class} non pris en charge.")


    def calculate_docs_to_answer_query_docs(self, query):
        # Obtenir tous les résultats du modèle
        all_results = self.model.calculate_docs_to_answer_query_docs(query)
        top_10_results = dict(list(all_results.items())[:10])
        return top_10_results
    
    ## Affichage des résultats à définir ici ?
    ######## A redéfinir dans les classes filles !

    def print(self, message: str):
        pass

    def model_choice(self):
        """Prompt user for model choice."""
        pass

    def launch_evaluation(self):
        """Launches the evaluation process."""
        pass

    @abstractmethod
    def run(self):
        """Runs the CLI interface."""
        pass