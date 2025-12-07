from numpy import dot
from numpy.linalg import norm
from heapq import nlargest

from src.back.search.domain.search_model import SearchModel
from src.back.search.infrastructure.searchrequirement.embedding_search_requirement import EmbeddingSearchRequirement

class EmbeddingSearchModel(SearchModel):
    
    def cosine_similarity(self, vector1, vector2):
        """Calcule la similarité cosinus entre deux vecteurs."""
        if norm(vector1) == 0 or norm(vector2) == 0:
            return 0.0
        return dot(vector1, vector2) / (norm(vector1) * norm(vector2))
    

    def calculate_docs_to_answer_query_docs(self, search_requirement: EmbeddingSearchRequirement):
        """
        Trouve les documents les plus pertinents pour une requête utilisateur.
        :param query: Texte brut de la requête utilisateur.
        :param top_n: Nombre de documents pertinents à retourner.
        :return: Liste de tuples (nom du fichier, score de similarité) des documents les plus pertinents.
        """
        # 1/3 - Calculer l'embedding de la requête
        query_embedding = search_requirement.get_document_vector_calculator().create_document_embedding(search_requirement.get_preprocessed_query())

        # 2/3 - Calculer la similarité entre la requête et chaque document 
        document_embeddings = search_requirement.get_document_embeddings().load()
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
        top_documents = nlargest(10, docs_to_answer_query.items(), key=lambda item: item[1])
        for tuple in top_documents:
            print(f"{tuple[0]}:{tuple[1]}")
        return docs_to_answer_query
