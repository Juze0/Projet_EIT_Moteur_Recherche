from numpy import zeros, mean, amax, concatenate

from src.file_handlers.file import File


class DocumentVectorCalculator():

    def __init__(self, max_docs=None):
        self.max_docs = max_docs
        self.document_embeddings = None # TODO Vérifie que le modèle de recherche cherche l'info différemment

    def create_mean_embedding(self, trained_model:File, words):
        """Calcule l'embedding moyen pour une liste de mots."""
        model = trained_model.load()
        word_vectors = [model[word] for word in words if word in model]
        if not word_vectors:
            return zeros(model.get_dimension())
        return mean(word_vectors, axis=0)


    def create_max_embedding(self, trained_model:File, words):
        """Calcule l'embedding max coordonné pour une liste de mots."""
        model = trained_model.load()
        word_vectors = [model[word] for word in words if word in model]
        if not word_vectors:
            return zeros(model.get_dimension())
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
        document_embeddings = {}
        for idx, line in enumerate(preprocessed_merged_corpus.load(use_iterator=True)):
            processed_words = line.strip().split()
            document_embedding = self.create_document_embedding(processed_words)
            document_embeddings[ordered_file_list[idx]] = document_embedding.tolist()
        self.document_embeddings = document_embeddings
        return document_embeddings
