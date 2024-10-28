from .preprocessor import Preprocessor

# SpaCy import part 
from spacy import load 

class SpaCyPreprocessor(Preprocessor):

    def __init__(self):
        super().__init__("spacy")
        self.nlp = load("fr_core_news_md")
        self.stopwords = set(self.nlp.Defaults.stop_words)

    def normalize_text(self, text):
        """
        Cette fonction prend un texte en paramètre et le normalise (retire la ponctuation, les espaces, les caractères spéciaux, les stopwords, etc.) en fonction de la librairie choisie.
        """
        token_list = []
        doc = self.nlp(text)
        for token in doc:
            if (token.text.lower() not in self.stopwords and not token.is_stop 
                    and token.is_alpha and self.regex.match(token.text)):
                token_list.append(token.text.lower())
        return token_list


    def normalize_document(self, file):
        """
        Prend un lien en paramètre et normalise le texte issu du lien afin de le normaliser (retire la ponctuation,
        les espaces, les caractères spéciaux, les stopwords, etc.)
        """
        token_list = []
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()  # Lire tout le fichier d'un coup
            doc = self.nlp(text)  # Traiter le texte entier
            
            for token in doc:
                if (token.text.lower() not in self.stopwords and not token.is_stop 
                        and token.is_alpha and self.regex.match(token.text)):
                    token_list.append(token.text.lower())  
        return token_list
    

    def lemmatize(self, tokens):
        """
        Prend une liste de tokens en paramètre et retourne les lemmes des tokens dans une liste.
        """
        lemmatized_tokens = []
        if tokens:  # Vérifie si la liste de tokens n'est pas vide
            doc = self.nlp(" ".join(tokens))
            for token in doc:
                lemmatized_tokens.append(token.lemma_)
        return lemmatized_tokens