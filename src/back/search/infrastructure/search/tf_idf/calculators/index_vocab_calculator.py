from collections import defaultdict

from src.back.search.infrastructure.search.calculator import Calculator
from src.back.core.application.ports.file import File
from src.back.preprocessor.domain.preprocessor import Preprocessor

class IndexAndVocabCalculator(Calculator):

    def __init__(self):
        super().__init__()


    def create_index(self, preprocessor: Preprocessor, files: list[File]):
        """
        Renvoie un index (normalisé et lemmatisé) associant les fichiers à leur liste de mots.
        """
        return { f.get_file_name(): preprocessor.normalize_then_lemmatize(f.load()) for f in files}
    
    
    def create_inversed_index(self, index_file: File):
        """
        Renvoie un index inversé associant les mots à leur occurence dans les documents.
        """
        index = index_file.load()
        inverse_index = defaultdict(lambda: defaultdict(int))
        for filename in index:
            for token in index[filename]:
                inverse_index[token][filename] += 1
        return inverse_index
    

    def extract_full_vocab(self, preprocessor: Preprocessor, files: list[File]):
        """
        Renvoie le vocabulaire complet (normalisé et lemmatisé) des fichiers.
        """
        full_vocab = set()
        for f in files:
            full_vocab.update(preprocessor.normalize_then_lemmatize(f.load()))
        return list(full_vocab)