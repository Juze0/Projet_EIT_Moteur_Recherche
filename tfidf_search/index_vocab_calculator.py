import os
from collections import defaultdict

from data.json_file_type import JSONFileType
from utils.result_file_ensurer import ResultFileEnsurer

class IndexAndVocabCalculator:

    def __init__(self, preprocessor):
        #### HERE THE ORDER MATTERS !!!
        self.preprocessor = preprocessor
        self.result_files_ensurer = ResultFileEnsurer({
            JSONFileType.INDEX:            self.create_index,
            JSONFileType.INVERSE_INDEX:    self.create_inversed_index,
            JSONFileType.FULL_VOCAB:       self.extract_full_vocab
        })
        self.result_files_ensurer.check_and_create_all("le vocabulaire, l'index et l'index inversé", self.preprocessor.name)
       
    def create_index(self):
        """
        Prend un dossier en paramètre et crée un index (dictionnaire) associant les fichiers à leur liste de mots normalisés et lemmatisés.
        """
        index = {}
        folder_name = JSONFileType.WIKI_FOLDER.value
        for filename in os.listdir(folder_name):
            f = os.path.join(folder_name, filename)
            if os.path.isfile(f) and f.endswith(".txt"):
                # library
                tokens_by_file = self.preprocessor.normalize_document(f)
                lemmatized_tokens = self.preprocessor.lemmatize(tokens_by_file)
                index[filename] = lemmatized_tokens
                # ---
        return index
    
    def create_inversed_index(self):
        """
        Prend un dossier en paramètre et renvoie un index inversé (dictionnaire) associant les mots à leur occurence dans les documents.
        """
        index = self.result_files_ensurer.load_json_using_enum(JSONFileType.INDEX, self.preprocessor.name)
        inverse_index = defaultdict(lambda: defaultdict(int))
        #index = self.create_index(directory_link, library_name)   => NORMALEMENT, il y aura un conflit sur les TYPES !!!!
        for filename in index:
            for token in index[filename]:
                inverse_index[token][filename] += 1
        return inverse_index
    
    def extract_full_vocab(self):
        """
        Prend un dossier de fichiers en paramètre et renvoie le vocabulaire complet (normalisé et lemmatisé) des fichiers.
        """
        full_vocab = set() #Permet d'éviter les doublons
        folder_name = JSONFileType.WIKI_FOLDER.value
        for filename in os.listdir(folder_name):
            f = os.path.join(folder_name, filename)
            if os.path.isfile(f) and f.endswith(".txt"):
                # library
                tokens_by_file = self.preprocessor.normalize_document(f)
                lemmatized_tokens = self.preprocessor.lemmatize(tokens_by_file)
                full_vocab.update(lemmatized_tokens)
                # ---
        return list(full_vocab)