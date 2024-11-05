import os
from collections import defaultdict

from src.search_models.calculator import Calculator
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.utils.result_file_ensurer import ResultFileEnsurer
from src.file_handlers.json_file_handler import JSONFileHandler

class IndexAndVocabCalculator(Calculator):

    def __init__(self, preprocessor):
        self.preprocessor = preprocessor
        self.result_files_ensurer = ResultFileEnsurer(self.get_file_processing_map(), JSONFileHandler())
        self.result_files_ensurer.check_and_create_all("le vocabulaire, l'index et l'index inversé", self.preprocessor.name)

    ### parent method to override
    def get_file_processing_map(self):
        """Retourne une carte associant les types de fichiers aux méthodes de traitement."""
        #### INTERN DEPENDENCIES => HERE THE ORDER MATTERS !!!
        return {
            FileHierarchyEnum.INDEX:            self.create_index,
            FileHierarchyEnum.INVERSE_INDEX:    self.create_inversed_index,
            FileHierarchyEnum.FULL_VOCAB:       self.extract_full_vocab,
        }

    ### all calculations methods
    def create_index(self):
        """
        Prend un dossier en paramètre et crée un index (dictionnaire) associant les fichiers à leur liste de mots normalisés et lemmatisés.
        """
        index = {}
        folder_name = FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER)
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
        index = self.result_files_ensurer.load_using_enum(FileHierarchyEnum.INDEX, self.preprocessor.name)
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
        folder_name = FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER)
        for filename in os.listdir(folder_name):
            f = os.path.join(folder_name, filename)
            if os.path.isfile(f) and f.endswith(".txt"):
                # library
                tokens_by_file = self.preprocessor.normalize_document(f)
                lemmatized_tokens = self.preprocessor.lemmatize(tokens_by_file)
                full_vocab.update(lemmatized_tokens)
                # ---
        return list(full_vocab)