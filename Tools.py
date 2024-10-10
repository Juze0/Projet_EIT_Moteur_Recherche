import os
import string
import re
import json
import spacy
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
    
    def lemmatize_nltk(self,tokens):
        """
        Prend une liste de tokens en paramètre et retourne une liste de tokens lemmatisés
        """
        lemmatized_tokens = []
        
        lemmatizer = self.lemmatizer
        for token in tokens:
            lemmatized_tokens.append(lemmatizer.stem(token))
        return lemmatized_tokens
    
    def create_index_nltk(self,directory_link, save_index = False):
        """
        Créé un index à partir d'un dossier de fichiers texte. Les fichiers sont tokenizés, normalisés et lemmatisés.
        Retourne un dictionnaire avec les documents et leurs lemmes.
        """
        index = {}
        for filename in os.listdir(directory_link):
            f = os.path.join(directory_link, filename)
            if os.path.isfile(f)and f.endswith(".txt"):
                tokens_by_file = self.normalize_document_nltk(f)
                lemmatized_tokens = self.lemmatize_nltk(tokens_by_file)
                index[filename] = lemmatized_tokens
        if save_index:
            with open("index_nltk.json", "w", encoding='utf-8') as f:
                json.dump(index, f, ensure_ascii=False, indent=4)
        return index
    
    def create_inversed_index_nltk(self,directory_link, save_index = False):
        """
        Cette fonction permet de créer un index inversé à partir d'un dossier de fichiers texte. Les fichiers sont tokenizés, normalisés et lemmatisés.
        Retourne un dictionnaire avec les mots et les documents dans lesquels ils apparaissent ainsi que leur nombre d'occurrences.
        """
        inverse_index = defaultdict(lambda: defaultdict(int)) #Permet de faciliter la création de l'index inversé qui est un dictionnaire de dictionnaires et continet les mots et les documents dans lesquels ils apparaissent ainsi que leur nombre d'occurrences
        index = self.create_index_nltk(directory_link)
        for filename in index: # Pour chaque fichier dans l'index
            for token in index[filename]: # Pour chaque token de la liste qui est dans le fichier
                inverse_index[token][filename] += 1 # On incrémente le nombre d'occurrences du token en construisant l'index inversé
        if save_index:
            with open("inverse_index_nltk.json", "w", encoding='utf-8') as f:
                json.dump(inverse_index, f, ensure_ascii=False, indent=4)
        return inverse_index
    
    def create_index_spacy(self, directory_link):
        """
        Créé un index à partir d'un dossier de fichiers texte. Les fichiers sont tokenizés, normalisés et lemmatisés.
        Retourne un dictionnaire avec les documents et leurs lemmes.
        """
        index = {}
        for filename in os.listdir(directory_link):
            f = os.path.join(directory_link, filename)
            if os.path.isfile(f) and f.endswith(".txt"):
                tokens_by_fic = self.normalize_document_spacy(f)
                lemmatized_tokens = self.lemmatize_spacy(tokens_by_fic)
                index[filename] = lemmatized_tokens

        return index

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
    
    def normalize_document_nltk_texts_from_folder(self,folder):
        """
        Prend un dossier en paramètre et normalise tous les textes du dossier
        """
        normalize_document_nltk_texts = []
        for file in os.listdir(folder):
            normalize_document_nltk_texts.append(Tools.normalize_document_nltk(folder + file))
        return normalize_document_nltk_texts
    
