from sklearn.metrics.pairwise import cosine_similarity

from data.json_file_type import JSONFileType
from data.json_file_handler import JSONFileHandler
from tfidf_search.index_vocab_calculator import IndexAndVocabCalculator
from tfidf_search.tf_idf_calculator import TFIDFCalculator

""" La lemmatisation avec Spacy est plus précise que celle de NLTK, on doit choisir entre les deux """

class TFIDFSearchModel:

    nlp = None

    def __init__(self, preprocessor):
        self.preprocessor = preprocessor
        # ORDER MATTERS (because of dependencies !!)
        self.vocab_idx_reverse_idx = IndexAndVocabCalculator(preprocessor)
        self.tf_idf = TFIDFCalculator(preprocessor.name)
        self.json_file_handler = JSONFileHandler()

    # ******** Data handler
    def load_json(self, json_file_type, remaining_name=""):
        return self.json_file_handler.load_json_using_enum(json_file_type, remaining_name)
    
    # ******** DEALING WITH USER REQUEST

    def preprocess_query(self, query):
        """
        Prend une requête utilisateur en paramètre et la normalise (retire la ponctuation, les espaces, les caractères spéciaux, les stopwords, etc.)
        Retourne une liste de tokens normalisés associés à la requête utilisateur.
        """
        query_tokens = []
        query_tokens = self.preprocessor.lemmatize(self.preprocessor.normalize_text(query))
        return query_tokens
    
    def calculate_docs_to_answer_query_docs(self, query):
        """
        Prend une requête utilisateur, le dictionnaire de tf*idf des documents et le dictionnaire des idf des mots.
        Retourne un dictionnaire associant les documents et leur similarité cosinus avec la requête utilisateur. Le dictionnaire est en ordre décroissant.
        """
        # [SPECIFIC ou ALL], j'essaye de comprendre ce qui est spéicifique à un model et ce qu'il ne l'est pas, pour aboutir, je l'espère à la forme de getDocumentsCorrespondingToReq(req, documents), en résumé, j'esssaye de comprendre ce qui est factorisable et ce qui ne l'est pas !
        # [SPECIFIC] Chargement des données nécessaires pour TF-IDF, ici `idf_dict` et `tf_idf_vectors`
        # Pour un autre modèle (Word Embeddings ou BERT), il chargerait ses propres données,
        # comme un espace vectoriel d'embeddings.
        idf_dict = self.load_json(JSONFileType.IDF, self.preprocessor.name)
        tf_idf_vectors = self.load_json(JSONFileType.TF_IDF_VECTORS, self.preprocessor.name)

        # [ALL] Prétraitement de la requête
        query_tokens = self.preprocess_query(query)
        query_tf = {}
        dict_tokens = self.count_words(query_tokens)
        nb_words = len(query_tokens)
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
        full_vocab = {}
        full_vocab = self.load_json(JSONFileType.FULL_VOCAB, self.preprocessor.name)
        
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
        for filename, vector in tf_idf_vectors.items():
           
            # Vérification que les dimensions sont compatibles avant de calculer la similarité
            if len(query_vector) == len(vector):
                docs_to_answer_query[filename] = cosine_similarity([query_vector], [vector])[0][0]
            else:
                print(f"Dimensions incompatibles pour le document '{filename}' : {len(query_vector)} vs {len(vector)}")

        # [ALL] Tri des résultats de recherche
        docs_to_answer_query = dict(sorted(docs_to_answer_query.items(), key=lambda x: x[1], reverse=True))
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
           self.save_as_json(word_count, JSONFileType.WORD_COUNT)
        return word_count