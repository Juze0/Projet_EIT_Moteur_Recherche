import spacy
import nltk 
import re
from nltk.corpus import stopwords
from collections import Counter

class Tools2:

    nlp = None

    def __init__(self):
        self.nlp = spacy.load("fr_core_news_md")

    
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
        for token in tokens:
            doc = self.nlp(token)
            for token in doc:
                lemmatized_tokens[token.lemma_] = token.pos_
        return lemmatized_tokens
    
    
    def count_words(self,tokens):
        """
        Prend un dictionnaire de tokens et POS spacy en paramètre et retourne un dictionnaire avec les mots et leur fréquence
        """
        word_count = {}
        for token in tokens:
            if token not in word_count:
                word_count[token] = 1
            elif token in word_count:
                word_count[token] += 1
        return word_count
