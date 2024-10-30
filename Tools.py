import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict

from data.json_handler import JSONHandler
from data.json_file_type import JSONFileType

""" La lemmatisation avec Spacy est plus précise que celle de NLTK, on doit choisir entre les deux """

class Tools:

    nlp = None

    def __init__(self, preprocessor):
        self.__preprocessor = preprocessor

    # ******** Preprocessor's methods
    def normalize_text(self, text):
        return self.__preprocessor.normalize_text(text)

    def normalize_document(self, file):
        return self.__preprocessor.normalize_document(file)

    def lemmatize(self, tokens):
        return self.__preprocessor.lemmatize(tokens)
    
    def get_preprocessor_name(self):
        return self.__preprocessor.name

    # ******** Data handler
    def save_as_json(self, data, file_name_prefix, preprocessor_name=""):
        JSONHandler.save_as_json(data, file_name_prefix, preprocessor_name)

    def load_json(self, file_name_prefix, preprocessor_name=""):
        return JSONHandler.load_json(file_name_prefix, preprocessor_name)
    
    def extract_full_vocab(self, directory_link, save_index=False):
        """
        Prend un dossier de fichiers en paramètre et renvoie le vocabulaire complet (normalisé et lemmatisé) des fichiers.
        """
        full_vocab = set() #Permet d'éviter les doublons
        for filename in os.listdir(directory_link):
            f = os.path.join(directory_link, filename)
            if os.path.isfile(f) and f.endswith(".txt"):
                # library
                tokens_by_file = self.normalize_document(f)
                lemmatized_tokens = self.lemmatize(tokens_by_file)
                full_vocab.update(lemmatized_tokens)
                # ---
        if save_index:
            self.save_as_json(list(full_vocab), JSONFileType.FULL_VOCAB, self.get_preprocessor_name())
        return full_vocab
    
    
    def create_index(self, directory_link, save_index=False):
        """
        Prend un dossier en paramètre et crée un index (dictionnaire) associant les fichiers à leur liste de mots normalisés et lemmatisés.
        """
        index = {}
        for filename in os.listdir(directory_link):
            f = os.path.join(directory_link, filename)
            if os.path.isfile(f) and f.endswith(".txt"):
                # library
                tokens_by_file = self.normalize_document(f)
                lemmatized_tokens = self.lemmatize(tokens_by_file)
                index[filename] = lemmatized_tokens
                # ---
        if save_index:
            self.save_as_json(index, JSONFileType.INDEX, self.get_preprocessor_name())
        return index
    
    def create_inversed_index(self, directory_link, save_index=False):
        """
        Prend un dossier en paramètre et renvoie un index inversé (dictionnaire) associant les mots à leur occurence dans les documents.
        """
        inverse_index = defaultdict(lambda: defaultdict(int))

        library_name = self.get_preprocessor_name()
        index = self.create_index(directory_link, library_name)
        for filename in index:
            for token in index[filename]:
                inverse_index[token][filename] += 1
        if save_index:
            self.save_as_json(inverse_index, JSONFileType.INVERSE_INDEX, self.get_preprocessor_name())
        return inverse_index
    
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
    
    def calculate_tf(self, index, save_index=False):
        """
        Prend un dictionnaire associant les fichiers à leur liste de mots.
        Retourne un dictionnaire associant les fichiers à leur liste de mots et leur fréquence normalisée.
        """
        tf = {}
        for filename in index:  # On itère sur les clés du dictionnaire index
            tf[filename] = {}  # On crée un dictionnaire vide pour chaque fichier, il contiendra les mots et leur fréquence
            count_words = len(index[filename])  # On compte le nombre de mots dans le fichier
            for token in index[filename]:  # On itère sur les tokens de chaque fichier dans l'index
                if token not in tf[filename]:
                    tf[filename][token] = 1
                else:
                    tf[filename][token] += 1
            for token in tf[filename]:
                tf[filename][token] = tf[filename][token] / count_words  # On divise le nombre d'occurrences de chaque mot par le nombre total de mots dans le fichier
        if save_index:
            self.save_as_json(tf, JSONFileType.TF, self.get_preprocessor_name())
        return tf
        
    def calculate_idf(self, inverse_index, save_index=False):
        """
        Prend un dictionnaire associant les mots à leur occurence dans les documents.
        Retourne un dictionnaire associant les mots à leur fréquence inverse de document.
        """
        idf = {}
        #index = self.load_json("inverse_index_" + library + ".json")
        nb_docs = len(inverse_index.keys()) #On compte le nombre de documents
        #nb_docs = len(inverse_index) #On compte le nombre de documents
        for token in inverse_index: #On itère sur les tokens de l'index inversé
            if token not in idf:
                idf[token] = np.log10(((nb_docs)/(len(inverse_index[token].keys()))) + 1) #On calcule le logarithme du nombre de documents divisé par le nombre de documents contenant le mot
        if save_index:
            self.save_as_json(idf, JSONFileType.IDF, self.get_preprocessor_name())
        return idf

    def calculate_tf_idf(self, tf_dict, idf_dict, save_index=False):
        """
        Prend un dictionnaire associant les fichiers à leurs mots avec fréquence normalisée 
        et un dictionnaire associant les mots à leur fréquence inverse de document (IDF).
        Retourne un dictionnaire associant les fichiers à leurs mots avec les scores TF-IDF.
        """
        tf_idf = {}
        #index_tf_idf = {}
        for filename, tokens in tf_dict.items(): #On itère sur les fichiers et leur liste de mots et leur fréquence
            tf_idf[filename] = {} #On crée un dictionnaire vide pour chaque fichier, il contiendra les mots et leur tf*idf
            #index_tf_idf[filename] = []
            for token, term_frequency in tokens.items(): #On itère sur les mots et leur fréquence dans chaque fichier
                if token in idf_dict:
                    tf_idf_score = term_frequency * idf_dict[token] #On calcule le tf*idf
                    tf_idf[filename][token] = tf_idf_score
                    #index_tf_idf[filename].append((tf_idf_score))
        if save_index:
            self.save_as_json(tf_idf, JSONFileType.TF_IDF, self.get_preprocessor_name())
        return tf_idf
    
    def create_tf_idf_vectors(self, tf_idf_dict, full_vocab, save_index=False):
        """
        Prend un dictionnaire associant les fichiers à leurs mots avec les scores TF-IDF et le vocabulaire complet.
        Retourne un dictionnaire associant les fichiers à leur vecteur TF-IDF.
        """
        tf_idf_vectors = {}
        print("Taille du vocabulaire : ", len(full_vocab))
        for filename, tokens in tf_idf_dict.items():
        # Initialiser un vecteur avec des zéros en tant que liste
            tf_idf_vectors[filename] = [0.0] * len(full_vocab)
            for i, token in enumerate(full_vocab):
                if token in tokens:
                    tf_idf_vectors[filename][i] = tokens[token]  # Remplir le vecteur avec le score TF-IDF
        if save_index:
            self.save_as_json(tf_idf_vectors, JSONFileType.TF_IDF_VECTORS, self.get_preprocessor_name())
        return tf_idf_vectors
    
    def search_documents_query_inversed_index(self, preprocessed_query, inverse_index):
        """
        Prend une requête utilisateur prétraitée et l'index inversé.
        Retourne un dictionnaire associant les documents et leur fréquence d'apparition dans la requête utilisateur.
        """

    def preprocess_query(self, query):
        """
        Prend une requête utilisateur en paramètre et la normalise (retire la ponctuation, les espaces, les caractères spéciaux, les stopwords, etc.)
        Retourne une liste de tokens normalisés associés à la requête utilisateur.
        """
        query_tokens = []
        query_tokens = self.lemmatize(self.normalize_text(query))
        return query_tokens
    
    def calculate_docs_to_answer_query_docs(self, query, tf_idf_vectors, idf_dict):
        """
        Prend une requête utilisateur, le dictionnaire de tf*idf des documents et le dictionnaire des idf des mots.
        Retourne un dictionnaire associant les documents et leur similarité cosinus avec la requête utilisateur. Le dictionnaire est en ordre décroissant.
        """
        query_tokens = self.preprocess_query(query)
        query_tf = {}
        dict_tokens = self.count_words(query_tokens)
        nb_words = len(query_tokens)
        print("Nombre de mots dans la requête : ", nb_words)
        print("Mots de la requête : ", dict_tokens)
        for token in dict_tokens:
            query_tf[token] = dict_tokens[token] / nb_words
            for tok in idf_dict:
                if token == tok:
                    print("IDF du mot ", token, " : ", idf_dict[tok])
                    query_tf[token] = query_tf[token] * idf_dict[tok]

        #print("Tokens de la requête : ")
        #print(query_tf)
        full_vocab = {}
        full_vocab = self.load_json(JSONFileType.FULL_VOCAB, self.get_preprocessor_name())
        
        query_vector = [0.0] * len(full_vocab)
        
        #print("Taille du vecteur de la requête : ", len(query_vector))
        for i, token in enumerate(full_vocab):
            if token in query_tf:
                query_vector[i] = query_tf[token]
        #print("Vecteur de la requête : ")
        #print(query_vector)
        
        docs_to_answer_query = {}
        for filename, vector in tf_idf_vectors.items():
            docs_to_answer_query[filename] = cosine_similarity([query_vector], [vector])[0][0]
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

    
