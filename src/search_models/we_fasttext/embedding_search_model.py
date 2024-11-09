from numpy import dot
from numpy.linalg import norm
from heapq import nlargest

from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.search_models.search_model import SearchModel
from src.search_models.we_fasttext.document_vector_calculator import DocumentVectorCalculator

class EmbeddingSearchModel(SearchModel):

    def __init__(self, preprocessor):
        #### EXTERN DEPENDENCIES !!!
        self.document_vector_calculator = DocumentVectorCalculator(preprocessor)
        #### -----------------------
        super().__init__(preprocessor)

    def preprocess_query(self, query):
        return self.preprocessor.normalize_text(query)


    def calculate_query_embedding(self, query):
        """Calcule l'embedding de la requête de l'utilisateur."""
        # Prétraiter la requête de l'utilisateur pour obtenir une liste de mots
        processed_words = self.preprocess_query(query)
        query_embedding = self.document_vector_calculator.create_document_embedding(processed_words)
        return query_embedding
    
    def cosine_similarity(self, vector1, vector2):
        """Calcule la similarité cosinus entre deux vecteurs."""
        if norm(vector1) == 0 or norm(vector2) == 0:
            return 0.0
        return dot(vector1, vector2) / (norm(vector1) * norm(vector2))
    

    def calculate_docs_to_answer_query_docs(self, query, top_n=10):
        """
        Trouve les documents les plus pertinents pour une requête utilisateur.
        :param query: Texte brut de la requête utilisateur.
        :param top_n: Nombre de documents pertinents à retourner.
        :return: Liste de tuples (nom du fichier, score de similarité) des documents les plus pertinents.
        """
        # 1/3 - Calculer l'embedding de la requête
        query_embedding = self.calculate_query_embedding(query)

        # 2/3 - Calculer la similarité entre la requête et chaque document
        document_embeddings = self.document_vector_calculator.result_files_ensurer.load_using_enum(FileHierarchyEnum.WE_FASSTEXT_DOCUMENT_EMBEDDINGS, self.preprocessor.name)
        
        docs_to_answer_query = {}
        for doc_name, doc_embedding in document_embeddings.items():
            # Vérification que les dimensions sont compatibles avant de calculer la similarité
            if len(query_embedding) == len(doc_embedding):
                similarity_score = self.cosine_similarity(query_embedding, doc_embedding)
                docs_to_answer_query[doc_name] = similarity_score
            else:
                print(f"Dimensions incompatibles pour le document '{doc_name}' : {len(query_embedding)} vs {len(doc_embedding)}")

        # 3/3 - Tri des résultats de recherche
        docs_to_answer_query = dict(sorted(docs_to_answer_query.items(), key=lambda x: x[1], reverse=True))
        #top_documents = nlargest(top_n, docs_to_answer_query.items(), key=lambda item: item[1])

        return docs_to_answer_query
