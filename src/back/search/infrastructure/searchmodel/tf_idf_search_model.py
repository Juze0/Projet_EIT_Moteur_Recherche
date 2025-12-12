from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest

from src.back.search.domain.search_model import SearchModel
from src.back.search.domain.search_query import SearchQuery
from src.back.search.infrastructure.search.dependencies.tf_idf_dependency import TfIdfDependency

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
        # [SPECIFIC ou ALL], j'essaye de comprendre ce qui est spéicifique à un model et ce qu'il ne l'est pas, pour aboutir, je l'espère à la forme de getDocumentsCorrespondingToReq(req, documents), en résumé, j'esssaye de comprendre ce qui est factorisable et ce qui ne l'est pas !
        # [SPECIFIC] Chargement des données nécessaires pour TF-IDF, ici `idf_dict` et `tf_idf_vectors`
        # Pour un autre modèle (Word Embeddings ou BERT), il chargerait ses propres données,
        # comme un espace vectoriel d'embeddings.

        # [ALL] Prétraitement de la requête
        idf_dict = self._model_dependency.get_idf().load()
        query_tf = {}
        dict_tokens = self.count_words(search_query.query)
        nb_words = len(search_query.query)
        print("Nombre de mots dans la requête : ", nb_words)
        print("Mots de la requête : ", dict_tokens)
        for token in dict_tokens:
            # [SPECIFIC] Calcul du TF de la requête spécifique à la méthode TF-IDF.
            # Pour Word Embeddings/BERT, cette étape pourrait différer : par exemple, on pourrait convertir la requête en un vecteur dense.
            query_tf[token] = dict_tokens[token] / nb_words

             # [SPECIFIC] Ici, on multiplie par l'IDF du token. Cette étape est spécifique à TF-IDF.
            # Un autre modèle pourrait appliquer une opération complètement différente (ou rien du tout).
            for tok in idf_dict:
                if token == tok:
                    print("IDF du mot ", token, " : ", idf_dict[tok])
                    query_tf[token] = query_tf[token] * idf_dict[tok]

        # [ALL] Préparation du vecteur de la requête
        #print("Tokens de la requête : ")
        #print(query_tf)
        full_vocab = self._model_dependency.get_full_vocab().load()
        query_vector = [0.0] * len(full_vocab)
        
        # [SPECIFIC] Construction du vecteur en utilisant des scores TF-IDF
        # Un autre modèle (comme BERT) pourrait ici créer un vecteur de densité différente ou utiliser un modèle d'embeddings pour cette étape.
        #print("Taille du vecteur de la requête : ", len(query_vector))
        for i, token in enumerate(full_vocab):
            if token in query_tf:
                query_vector[i] = query_tf[token]  # [SPECIFIC ou ALL ???]

        #print("Vecteur de la requête : ")
        #print(query_vector)
        
        # [SPECIFIC] Utilisation de la similarité cosinus pour TF-IDF (sauf si un autre modèle aussi utilise cosinus).
        # Par exemple, Word Embeddings ou BERT peuvent aussi utiliser cosinus, mais certains modèles peuvent opter pour d’autres mesures.
        docs_to_answer_query = {}
        for filename, vector in self._model_dependency.get_tf_idf_vectors().load().items():
           
            # Vérification que les dimensions sont compatibles avant de calculer la similarité
            if len(query_vector) == len(vector):
                docs_to_answer_query[filename] = cosine_similarity([query_vector], [vector])[0][0]
            else:
                print(f"Dimensions incompatibles pour le document '{filename}' : {len(query_vector)} vs {len(vector)}")

        # [ALL] Tri des résultats de recherche
        docs_to_answer_query = dict(sorted(docs_to_answer_query.items(), key=lambda x: x[1], reverse=True))
        top_documents = nlargest(10, docs_to_answer_query.items(), key=lambda item: item[1])
        for tuple in top_documents:
            print(f"{tuple[0]}:{tuple[1]}")
        return docs_to_answer_query

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