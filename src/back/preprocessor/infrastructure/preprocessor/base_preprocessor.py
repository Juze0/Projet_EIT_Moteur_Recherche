from re import compile, UNICODE
from src.back.preprocessor.domain.preprocessor import Preprocessor

class BasePreprocessor(Preprocessor):

    def __init__(self):
        self.regex = compile(r"^[\wÀ-ÿ]+$", UNICODE) # Regex pour les mots français avec caractères spéciaux