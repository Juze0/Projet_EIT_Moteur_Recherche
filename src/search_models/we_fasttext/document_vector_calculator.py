from numpy import zeros, mean, amax, concatenate

from src.search_models.calculator import Calculator
from src.file_handlers.file import File


class DocumentVectorCalculator(Calculator):

    def __init__(self, embedding_model_file:File, max_docs=None):
        super().__init__()
        self.embedding_model_file = embedding_model_file
        self.embedding_model = None
        self.max_docs = max_docs


    def create_mean_embedding(self, words):
        """Calcule l'embedding moyen pour une liste de mots."""
        word_vectors = [self.embedding_model[word] for word in words if word in self.embedding_model]
        if not word_vectors:
            return zeros(self.embedding_model.get_dimension())
        return mean(word_vectors, axis=0)


    def create_max_embedding(self, words):
        """Calcule l'embedding max coordonné pour une liste de mots."""
        word_vectors = [self.embedding_model[word] for word in words if word in self.embedding_model]
        if not word_vectors:
            return zeros(self.embedding_model.get_dimension())
        return amax(word_vectors, axis=0)


    def create_document_embedding(self, words):
        """Calcule l'embedding d'un document en concaténant les embeddings moyen et max coordonné.
        :param words: liste de mots du document
        :return: Le vecteur renvoyé est de dimension 2 * d et réprésente le document
        """
        return concatenate([self.create_mean_embedding(words), self.create_max_embedding(words)])


    def calculate_embeddings_for_all_documents(self, preprocessed_merged_corpus: File, ordered_file_list: list[str]):
        """Calcule les embeddings pour chaque document pré-traité dans le fichier unique de corpus."""
        if (self.embedding_model == None): self.embedding_model = self.embedding_model_file.load()
        document_embeddings = {}
        for idx, line in enumerate(preprocessed_merged_corpus.load(use_iterator=True)):
            processed_words = line.strip().split()
            document_embedding = self.create_document_embedding(processed_words)
            document_embeddings[ordered_file_list[idx]] = document_embedding.tolist()
        self.document_embeddings = document_embeddings
        return document_embeddings
