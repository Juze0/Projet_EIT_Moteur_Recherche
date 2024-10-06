import os
import string
import re
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


""" La lemmatisation avec Spacy est plus précise que celle de NLTK, on doit choisir entre les deux """

class Tools:

    nlp = None

    def __init__(self):
        self.nlp = spacy.load("fr_core_news_md")
        pass

    def normalize_nltk(self,link):
        """
        Prend un lien en paramètre et normalise le texte issu du lien afin de le normaliser (retire la ponctuation
        les espaces, les caractères spéciaux, les stopwords etc.)
        """
        #new_file = open(link + "_normalize_nltk.txt", "x")
        token_list = []
        regex = re.compile(r"^[\wÀ-ÿ]+$", re.UNICODE) # Regex pour les mots français avec caractères spéciaux
        with open(link, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.lower() # Met en minuscule
                line = word_tokenize(line, "french") # Tokenize le texte
                line = [word for word in line if word not in stopwords.words("french") and regex.match(word)] # Retire les stopwords (déterminants, mots de liaison...) et garde les mots français avec caractères spéciaux 
                token_list.extend(line)
        return token_list
    
    def lemmatize_nltk(self,tokens):
        """
        Prend une liste de tokens en paramètre et retourne une liste de tokens lemmatisés
        """
        lemmatized_tokens = []
        lemmatizer = SnowballStemmer("french")
        for token in tokens:
            lemmatized_tokens.append(lemmatizer.stem(token))
        return lemmatized_tokens
    
    def normalize_spacy(self,link):
        """
        Prend un lien en paramètre et normalise le texte issu du lien afin de le normaliser (retire la ponctuation
        les espaces, les caractères spéciaux, les stopwords etc.)
        """
        
        token_list = []
        regex = re.compile(r"^[\wÀ-ÿ]+$", re.UNICODE) # Regex pour les mots français avec caractères spéciaux
        with open(link, 'r', encoding='utf-8') as file:
            for line in file:
                doc = self.nlp(line)
                for token in doc:
                    if token.text not in stopwords.words('french') and not token.is_stop and token.is_alpha and regex.match(token.text): #Double passage dans des stopwords différent pour bien les filtrer
                        token_list.append(token.text.lower())
        return token_list
    
    
    def lemmatize_spacy(self,tokens):
        """
        Prend une liste de tokens en paramètre et retourne les lemmes des tokens avec leur POS dans un dictionnaire
        """
        lemmatized_tokens = {}
        doc = self.nlp(" ".join(tokens))
        for token in doc:
            lemmatized_tokens[token.lemma_] = token.pos_
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
    
    def normalize_nltk_texts_from_folder(self,folder):
        """
        Prend un dossier en paramètre et normalise tous les textes du dossier
        """
        normalize_nltk_texts = []
        for file in os.listdir(folder):
            normalize_nltk_texts.append(Tools.normalize_nltk(folder + file))
        return normalize_nltk_texts
    
