from os import listdir
from os.path import join
from numpy import zeros, mean, amax, concatenate

from numpy import dot
from numpy.linalg import norm
from heapq import nlargest


from src.search_models.calculator import Calculator
from src.search_models.we_fasttext.we_calculator import WECalculator

from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.file_handlers.json_file_handler import JSONFileHandler

class DocumentVectorCalculator(Calculator):

    def __init__(self, preprocessor, max_docs=None):
        self.max_docs = max_docs
        #### EXTERN DEPENDENCIES !!!
        self.word_embeddings_calculator = WECalculator(preprocessor, "skipgram", max_docs)
        self.model = self.word_embeddings_calculator.model
        #### -----------------------
        super().__init__(preprocessor, JSONFileHandler(), "les embeddings de chaque document du corpus !")
        self.document_embeddings = None

    ### Method of Calculator class to override
    def get_file_processing_map(self):
        """Retourne une carte associant les types de fichiers aux méthodes de traitement."""
        #### INTERN DEPENDENCIES => HERE THE ORDER MATTERS !!!
        return {
            FileHierarchyEnum.WE_FASSTEXT_DOCUMENT_EMBEDDINGS:  self.calculate_embeddings_for_all_documents,
        }

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


    def calculate_embeddings_for_all_documents(self):
        """Calcule les embeddings pour chaque document pré-traité dans le fichier unique de corpus."""
        wiki_folder_path = FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER)
        file_list = sorted(listdir(wiki_folder_path))[:self.max_docs] if self.max_docs is not None else sorted(listdir(wiki_folder_path))
        # La fonction preprocess_and_merge_texts de WECalculator a elle aussi utilisé l'ordre alphabétique !!!

        preprocessed_texts_file_path = FileHierarchyEnum.get_file_path(FileHierarchyEnum.WE_PREPROCESSED_MERGED_CORPUS, self.preprocessor_name)
        document_embeddings = {}
        with open(preprocessed_texts_file_path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                processed_words = line.strip().split()  # Chaque ligne est déjà pré-traitée en une liste de mots
                document_embedding = self.create_document_embedding(processed_words)
                document_embeddings[file_list[idx]] = document_embedding.tolist()
        self.document_embeddings = document_embeddings
        return document_embeddings
