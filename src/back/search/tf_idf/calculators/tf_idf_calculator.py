from numpy import log10

from src.back.search.shared.calculator import Calculator
from src.back.search.application.ports.persistence.file import File

class TFIDFCalculator(Calculator):

    def __init__(self):
        super().__init__()
    
    def calculate_tf(self, index_file: File):
        """
        Prend un dictionnaire associant les fichiers à leur liste de mots.
        Retourne un dictionnaire associant les fichiers à leur liste de mots et leur fréquence normalisée.
        """
        index = index_file.load()
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
        return tf
        
    def calculate_idf(self, inverse_index_file: File):
        """
        Prend un dictionnaire associant les mots à leur occurence dans les documents.
        Retourne un dictionnaire associant les mots à leur fréquence inverse de document.
        """
        inverse_index = inverse_index_file.load()
        idf = {}
        nb_docs = len(inverse_index.keys()) #On compte le nombre de documents
        for token in inverse_index: #On itère sur les tokens de l'index inversé
            if token not in idf:
                idf[token] = log10(((nb_docs)/(len(inverse_index[token].keys()))) + 1) #On calcule le logarithme du nombre de documents divisé par le nombre de documents contenant le mot
        return idf

    def calculate_tf_idf(self, tf_file: File, idf_file: File):
        """
        Prend un dictionnaire associant les fichiers à leurs mots avec fréquence normalisée 
        et un dictionnaire associant les mots à leur fréquence inverse de document (IDF).
        Retourne un dictionnaire associant les fichiers à leurs mots avec les scores TF-IDF.
        """
        tf_dict = tf_file.load()
        idf_dict = idf_file.load()

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
        return tf_idf
    
    def create_tf_idf_vectors(self, tf_idf_file: File, full_vocab_file: File):
        """
        Prend un dictionnaire associant les fichiers à leurs mots avec les scores TF-IDF et le vocabulaire complet.
        Retourne un dictionnaire associant les fichiers à leur vecteur TF-IDF.
        """
        tf_idf_dict = tf_idf_file.load()
        full_vocab = full_vocab_file.load()

        tf_idf_vectors = {}
        print("Taille du vocabulaire : ", len(full_vocab))
        for filename, tokens in tf_idf_dict.items():
        # Initialiser un vecteur avec des zéros en tant que liste
            tf_idf_vectors[filename] = [0.0] * len(full_vocab)
            for i, token in enumerate(full_vocab):
                if token in tokens:
                    tf_idf_vectors[filename][i] = tokens[token]  # Remplir le vecteur avec le score TF-IDF
        return tf_idf_vectors