from os import listdir
from numpy import zeros, mean, amax, concatenate

from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.shared.files.file import File


class DocumentVectorCalculator():

    def __init__(self, preprocessor, max_docs=None):
        self.max_docs = max_docs
        self.model = self.word_embeddings_calculator.model
        self.preprocessor = preprocessor
        self.document_embeddings = None

    def create_mean_embedding(self, words):
        """Calcule l'embedding moyen pour une liste de mots."""
        word_vectors = [self.model[word] for word in words if word in self.model]
        if not word_vectors:
            return zeros(self.model.get_dimension())
        return mean(word_vectors, axis=0)


    def create_max_embedding(self, words):
        """Calcule l'embedding max coordonné pour une liste de mots."""
        word_vectors = [self.model[word] for word in words if word in self.model]
        if not word_vectors:
            return zeros(self.model.get_dimension())
        return amax(word_vectors, axis=0)


    def create_document_embedding(self, words):
        """Calcule l'embedding d'un document en concaténant les embeddings moyen et max coordonné.
        
        :param words: liste de mots du document
        :return: /!\ Le vecteur renvoyé est de dimension 2 * d et réprésente le document
        """
        mean_embedding = self.create_mean_embedding(words)
        max_embedding = self.create_max_embedding(words)
        return concatenate([mean_embedding, max_embedding])


    def calculate_embeddings_for_all_documents(self, preprocessed_merged_corpus: File, ordered_file_list: list[str]):
        """Calcule les embeddings pour chaque document pré-traité dans le fichier unique de corpus."""
        # La fonction preprocess_and_merge_texts de WECalculator a elle aussi utilisé l'ordre alphabétique !!!
        document_embeddings = {}
        for idx, line in enumerate(preprocessed_merged_corpus.iter_lines()):
            processed_words = line.strip().split()  # Chaque ligne est déjà pré-traitée en une liste de mots
            document_embedding = self.create_document_embedding(processed_words)
            document_embeddings[ordered_file_list[idx]] = document_embedding.tolist()
        self.document_embeddings = document_embeddings
        return document_embeddings
