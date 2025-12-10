from src.back.preprocessor.domain.preprocessor import Preprocessor
from src.back.preprocessor.domain.preprocessor_name import PreprocessorName

from src.back.preprocessor.infrastructure.preprocessor.spacy_preprocessor import SpaCyPreprocessor
from src.back.preprocessor.infrastructure.preprocessor.nltk_preprocessor import NLTKPreprocessor

class PreprocessorFactory():

    _preprocessor_map = {
        "nltk": NLTKPreprocessor,
        "spacy": SpaCyPreprocessor
    }

    def get_preprocessor(self, preprocessor_name: PreprocessorName) -> Preprocessor:
        if preprocessor_name.value not in self._preprocessor_map:
            raise ValueError(f"Preprocessor '{preprocessor_name.value}' is not recognized by the factory but is known by business rule!")
        return self._preprocessor_map[preprocessor_name.value]()