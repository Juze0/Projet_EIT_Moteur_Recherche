from numpy import dot
from numpy.linalg import norm
from heapq import nlargest

from src.back.search.domain.search_model import SearchModel
from src.back.search.domain.search_query import SearchQuery
from src.back.search.infrastructure.search.embedding.embedding_dependency import EmbeddingDependency
from src.back.search.application.dtos.search_response_dto import SearchResponseDTO, SearchResultDTO

class EmbeddingSearchModel(SearchModel):

    def __init__(self, model_dependency: EmbeddingDependency):
        self._model_dependency = model_dependency
    
    
    def cosine_similarity(self, vector1, vector2):
        """Calcule la similarité cosinus entre deux vecteurs."""
        if norm(vector1) == 0 or norm(vector2) == 0:
            return 0.0
        return dot(vector1, vector2) / (norm(vector1) * norm(vector2))
    

    def calculate_docs_to_answer_query_docs(self, search_query: SearchQuery):
        """
        Trouve les documents les plus pertinents pour une requête utilisateur.
        :param query: Texte brut de la requête utilisateur.
        :param top_n: Nombre de documents pertinents à retourner.
        :return: Liste de tuples (nom du fichier, score de similarité) des documents les plus pertinents.
        """
        # 1/3 - Calculer l'embedding de la requête
        query_embedding = self._model_dependency.get_document_vector_calculator().create_document_embedding(search_query.query)

        # 2/3 - Calculer la similarité entre la requête et chaque document 
        document_embeddings = self._model_dependency.get_document_embeddings().load()
        docs_scores = {}
        for doc_name, doc_embedding in document_embeddings.items():
            # Vérification que les dimensions sont compatibles avant de calculer la similarité
            if len(query_embedding) == len(doc_embedding):
                similarity_score = self.cosine_similarity(query_embedding, doc_embedding)
                docs_scores[doc_name] = similarity_score
            else:
                print(f"Dimensions incompatibles pour le document '{doc_name}' : {len(query_embedding)} vs {len(doc_embedding)}")

        top_documents = nlargest(search_query.top_n, docs_scores.items(), key=lambda item: item[1])
        results = [ SearchResultDTO(document_name=doc,  score=score) for doc, score in top_documents ]
        return SearchResponseDTO(
            query=search_query.query,
            results=results
        )
