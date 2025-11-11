from collections import defaultdict

from src.shared.files.file import File

class IndexAndVocabCalculator():

    def __init__(self, preprocessor):
        self.preprocessor = preprocessor

    # TODO: A remonter dans le preprocessor
    def normalize_and_lemmatize(self, content: str) -> str:
        return self.preprocessor.lemmatize(self.preprocessor.normalize_text(content))
         

    ### all calculations methods
    def create_index(self, files: list[File]):
        """
        Renvoie un index (normalisé et lemmatisé) associant les fichiers à leur liste de mots.
        """
        return { f.get_file_name(): self.normalize_and_lemmatize(f.load_text_content()) for f in files}
    
    
    def create_inversed_index(self, index_file: File):
        """
        Renvoie un index inversé associant les mots à leur occurence dans les documents.
        """
        index = index_file.load_json_content()
        inverse_index = defaultdict(lambda: defaultdict(int))
        for filename in index:
            for token in index[filename]:
                inverse_index[token][filename] += 1
        return inverse_index
    

    def extract_full_vocab(self, files: list[File]):
        """
        Renvoie le vocabulaire complet (normalisé et lemmatisé) des fichiers.
        """
        full_vocab = set()
        for f in files:
            full_vocab.update(self.normalize_and_lemmatize(f.load_text_content()))
        return list(full_vocab)