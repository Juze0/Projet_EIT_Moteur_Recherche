from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest

from src.back.search.domain.search_model import SearchModel
from src.back.search.domain.search_query import SearchQuery
from src.back.search.infrastructure.search.tf_idf.tf_idf_dependency import TfIdfDependency
from src.back.search.application.dtos.search_response_dto import SearchResponseDTO, SearchResultDTO

""" La lemmatisation avec Spacy est plus précise que celle de NLTK, on doit choisir entre les deux """

class TFIDFSearchModel(SearchModel):

    nlp = None

    def __init__(self, model_dependency: TfIdfDependency):
        self._model_dependency = model_dependency
    
   
    def calculate_docs_to_answer_query_docs(self, search_query: SearchQuery):
        """
        Prend une requête utilisateur, le dictionnaire de tf*idf des documents et le dictionnaire des idf des mots.
        Retourne un dictionnaire associant les documents et leur similarité cosinus avec la requête utilisateur. Le dictionnaire est en ordre décroissant.
        """

        idf_dict = self._model_dependency.get_idf().load()
        query_tf = {}
        dict_tokens = self.count_words(search_query.query)
        nb_words = len(search_query.query)
        print("Nombre de mots dans la requête : ", nb_words)
        print("Mots de la requête : ", dict_tokens)
        for token in dict_tokens:
            query_tf[token] = dict_tokens[token] / nb_words

            for tok in idf_dict:
                if token == tok:
                    print("IDF du mot ", token, " : ", idf_dict[tok])
                    query_tf[token] = query_tf[token] * idf_dict[tok]

        full_vocab = self._model_dependency.get_full_vocab().load()
        query_vector = [0.0] * len(full_vocab)
        
        for i, token in enumerate(full_vocab):
            if token in query_tf:
                query_vector[i] = query_tf[token]

        docs_scores = {}
        for filename, vector in self._model_dependency.get_tf_idf_vectors().load().items():
           
            if len(query_vector) == len(vector):
                docs_scores[filename] = cosine_similarity([query_vector], [vector])[0][0]
            else:
                print(f"Dimensions incompatibles pour le document '{filename}' : {len(query_vector)} vs {len(vector)}")

        top_documents = nlargest(search_query.top_n, docs_scores.items(), key=lambda item: item[1])
        results = [ SearchResultDTO(document_name=doc, score=score) for doc, score in top_documents ]
        return SearchResponseDTO(
            query=search_query.query,
            results=results
        )

    def count_words(self,tokens):
        """
        Prend une liste de tokens en paramètre et retourne un dictionnaire avec les mots et leur fréquence
        """
        word_count = {}
        for token in tokens:
            if token not in word_count:
                word_count[token] = 1
            elif token in word_count:
                word_count[token] += 1
        return word_count


    # ******** OTHERS FUNCTIONS (do we reeally need to keep them ???)
    def search_documents_query_inversed_index(self, preprocessed_query, inverse_index):
        """
        Prend une requête utilisateur prétraitée et l'index inversé.
        Retourne un dictionnaire associant les documents et leur fréquence d'apparition dans la requête utilisateur.
        """

    def create_dict_word_count(self, index, save_index=False):
        """
        Prend un dictionnaire associant les fichiers à leur liste de mots
        Retourne un dictionnaire associant les fichiers à leur liste de mots et leur occurence.
        """
        word_count = {}
        for filename in index:
            word_count[filename] = self.count_words(index[filename])
        if save_index:
           # TODO self.save_as_json(word_count, FileHierarchyEnum.WORD_COUNT)
           pass
        return word_count