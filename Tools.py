import os
import string
import re
import json
import spacy
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import defaultdict


""" La lemmatisation avec Spacy est plus précise que celle de NLTK, on doit choisir entre les deux """

class Tools:

    nlp = None

    def __init__(self):
        self.nlp = spacy.load("fr_core_news_md")
        self.stopwords = set(stopwords.words("french"))
        self.regex = re.compile(r"^[\wÀ-ÿ]+$", re.UNICODE) # Regex pour les mots français avec caractères spéciaux
        self.lemmatizer = SnowballStemmer("french")

    def normalize_document_nltk(self,file):
        """
        Prend un lien en paramètre et normalise le texte issu du lien afin de le normaliser (retire la ponctuation
        les espaces, les caractères spéciaux, les stopwords etc.)
        Retourne une liste de tokens normalisés associés au fichier link
        """
        #new_file = open(link + "_normalized.txt", "x")
        token_list = []
        #for filename in os.listdir(directory_link):
            #f = os.path.join(directory_link, filename)
            #if os.path.isfile(f)and f.endswith(".txt"):
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.lower() # Met en minuscule
                line = word_tokenize(line, "french") # Tokenize le texte
                line = [word for word in line if word not in self.stopwords and self.regex.match(word)] # Retire les stopwords (déterminants, mots de liaison...) et garde les mots français avec caractères spéciaux 
                token_list.extend(line)
        return token_list
    
    def normalize_text(self, text, library='nltk'):
        """
        Cette fonction prend un texte en paramètre et le normalise (retire la ponctuation, les espaces, les caractères spéciaux, les stopwords, etc.) en fonction de la librairie choisie.
        """
        token_list = []
        if library == 'nltk':
            text = text.lower()
            text = word_tokenize(text, "french")
            text = [word for word in text if word not in self.stopwords and self.regex.match(word)]
            token_list.extend(text)
        elif library == 'spacy':
            doc = self.nlp(text)
            for token in doc:
                if (token.text.lower() not in self.stopwords and not token.is_stop 
                        and token.is_alpha and self.regex.match(token.text)):
                    token_list.append(token.text.lower())
        return token_list
    
    def extract_full_vocab(self, directory_link, library='nltk', save_index=False):
        """
        Prend un dossier de fichiers en paramètre et renvoie le vocabulaire complet (normalisé et lemmatisé) des fichiers.
        """
        full_vocab = set() #Permet d'éviter les doublons
        for filename in os.listdir(directory_link):
            f = os.path.join(directory_link, filename)
            if os.path.isfile(f) and f.endswith(".txt"):
                if library == 'nltk':
                    tokens_by_file = self.normalize_document_nltk(f)
                    lemmatized_tokens = self.lemmatize_nltk(tokens_by_file)
                    full_vocab.update(lemmatized_tokens)
                elif library == 'spacy':
                    tokens_by_file = self.normalize_document_spacy(f)
                    lemmatized_tokens = self.lemmatize_spacy(tokens_by_file)
                    full_vocab.update(lemmatized_tokens)
        if save_index:
            with open("full_vocab_" + library + ".json", "w", encoding='utf-8') as f:
                json.dump(list(full_vocab), f, ensure_ascii=False, indent=4)
        return full_vocab
    
    def lemmatize_nltk(self,tokens):
        """
        Prend une liste de tokens en paramètre et retourne une liste de tokens lemmatisés
        """
        lemmatized_tokens = []
        
        lemmatizer = self.lemmatizer
        for token in tokens:
            lemmatized_tokens.append(lemmatizer.stem(token))
        return lemmatized_tokens
    
    def create_index(self, directory_link, library='nltk', save_index=False):
        """
        Prend un dossier en paramètre et crée un index (dictionnaire) associant les fichiers à leur liste de mots normalisés et lemmatisés.
        """
        index = {}
        for filename in os.listdir(directory_link):
            f = os.path.join(directory_link, filename)
            if os.path.isfile(f) and f.endswith(".txt"):
                if library == 'nltk':
                    tokens_by_file = self.normalize_document_nltk(f)
                    lemmatized_tokens = self.lemmatize_nltk(tokens_by_file)
                    index[filename] = lemmatized_tokens
                    name = "index_nltk.json"
                elif library == 'spacy':
                    tokens_by_file = self.normalize_document_spacy(f)
                    lemmatized_tokens = self.lemmatize_spacy(tokens_by_file)
                    index[filename] = lemmatized_tokens
                    name = "index_spacy.json"

        if save_index:
            with open(name, "w", encoding='utf-8') as f:
                json.dump(index, f, ensure_ascii=False, indent=4)
        return index
    
    def load_json(self, name):
        """
        Prend le nom d'un fichier json en paramètre et renvoie le dictionnaire associé.
        """
        with open(name, "r", encoding='utf-8') as f:
            index = json.load(f)
        return index
    
    def create_inversed_index(self, directory_link, library='nltk', save_index=False):
        """
        Prend un dossier en paramètre et renvoie un index inversé (dictionnaire) associant les mots à leur occurence dans les documents.
        """
        inverse_index = defaultdict(lambda: defaultdict(int))
        index = self.create_index(directory_link, library)
        name = "inverse_index_" + library + ".json"
        for filename in index:
            for token in index[filename]:
                inverse_index[token][filename] += 1
        if save_index:
            with open(name, "w", encoding='utf-8') as f:
                json.dump(inverse_index, f, ensure_ascii=False, indent=4)
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
            with open("word_count.json", "w", encoding='utf-8') as f:
                json.dump(word_count, f, ensure_ascii=False, indent=4)
        return word_count
    
    def calculate_tf(self, index, library='nltk',save_index=False):
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
            with open("tf_" + library + ".json", "w", encoding='utf-8') as f:
                json.dump(tf, f, ensure_ascii=False, indent=4)
        return tf
        
    def calculate_idf(self, inverse_index, library='nltk', save_index=False):
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
            with open("idf_" + library + ".json", "w", encoding='utf-8') as f:
                json.dump(idf, f, ensure_ascii=False, indent=4)
        return idf

    def calculate_tf_idf(self, tf_dict, idf_dict, library='nltk', save_index=False):
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
            with open("tf_idf_" +library +".json", "w", encoding='utf-8') as f:
                json.dump(tf_idf, f, ensure_ascii=False, indent=4)
        return tf_idf
    
    def create_tf_idf_vectors(self, tf_idf_dict, full_vocab, library="nltk", save_index=False):
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
            with open("tf_idf_" + library + "_vectors.json", "w", encoding='utf-8') as f:
                json.dump(tf_idf_vectors, f, ensure_ascii=False, indent=4)
        return tf_idf_vectors
    
    def search_documents_query_inversed_index(self, preprocessed_query, inverse_index, library='nltk'):
        """
        Prend une requête utilisateur prétraitée et l'index inversé.
        Retourne un dictionnaire associant les documents et leur fréquence d'apparition dans la requête utilisateur.
        """

    def preprocess_query(self, query, library='nltk'):
        """
        Prend une requête utilisateur en paramètre et la normalise (retire la ponctuation, les espaces, les caractères spéciaux, les stopwords, etc.)
        Retourne une liste de tokens normalisés associés à la requête utilisateur.
        """
        query_tokens = []
        if library == 'nltk':
            query_tokens = self.normalize_text(query, library)
            query_tokens = self.lemmatize_nltk(query_tokens)

        elif library == 'spacy':
            query_tokens = self.normalize_text(query, library) 
            query_tokens = self.lemmatize_spacy(query_tokens)
        return query_tokens
    
    def calculate_docs_to_answer_query_docs(self, query, tf_idf_vectors, idf_dict, library='nltk'):
        """
        Prend une requête utilisateur, le dictionnaire de tf*idf des documents et le dictionnaire des idf des mots.
        Retourne un dictionnaire associant les documents et leur similarité cosinus avec la requête utilisateur. Le dictionnaire est en ordre décroissant.
        """
        query_tokens = self.preprocess_query(query,library)
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
        if library == 'nltk':
            full_vocab = self.load_json("./json_files_for_tf_idf/full_vocab_nltk.json")
        elif library == 'spacy':
            full_vocab = self.load_json("./json_files_for_tf_idf/full_vocab_spacy.json")
          
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

        
        

    def normalize_document_spacy(self, link):
        """
        Prend un lien en paramètre et normalise le texte issu du lien afin de le normaliser (retire la ponctuation,
        les espaces, les caractères spéciaux, les stopwords, etc.)
        """
        token_list = []
        with open(link, 'r', encoding='utf-8') as file:
            text = file.read()  # Lire tout le fichier d'un coup
            doc = self.nlp(text)  # Traiter le texte entier
            
            for token in doc:
                if (token.text.lower() not in self.stopwords and not token.is_stop 
                        and token.is_alpha and self.regex.match(token.text)):
                    token_list.append(token.text.lower())  
        return token_list

    def lemmatize_spacy(self, tokens):
        """
        Prend une liste de tokens en paramètre et retourne les lemmes des tokens dans une liste.
        """
        lemmatized_tokens = []
        if tokens:  # Vérifie si la liste de tokens n'est pas vide
            doc = self.nlp(" ".join(tokens))
            for token in doc:
                lemmatized_tokens.append(token.lemma_)
        return lemmatized_tokens
    
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

    
