from .preprocessor import Preprocessor

# NLTK import part 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

class NLTKPreprocessor(Preprocessor):

    def __init__(self):
        super().__init__("nltk")
        self.stopwords = set(stopwords.words("french"))
        self.lemmatizer = SnowballStemmer("french")

    def normalize_text(self, text):
        """
        Cette fonction prend un texte en paramètre et le normalise (retire la ponctuation, les espaces, les caractères spéciaux, les stopwords, etc.) en fonction de la librairie choisie.
        """
        token_list = []
        text = text.lower()
        text = word_tokenize(text, "french")
        text = [word for word in text if word not in self.stopwords and self.regex.match(word)]
        token_list.extend(text)
        return token_list

    def normalize_document(self, file):
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
    

    def lemmatize(self, tokens):
        """
        Prend une liste de tokens en paramètre et retourne une liste de tokens lemmatisés
        """
        lemmatized_tokens = []
        
        lemmatizer = self.lemmatizer
        for token in tokens:
            lemmatized_tokens.append(lemmatizer.stem(token))
        return lemmatized_tokens