from src.back.search.domain.search_requirement import SearchRequirement
from src.back.file_handlers.file import File

class TfIdfSearchRequirement(SearchRequirement):

    def __init__(self, query: str, top_n: int, idf_dict:File, tf_idf_vectors:File, full_vocab:File):
        super().__init__(query, top_n)
        self._idf_dict = idf_dict
        self._tf_idf_vectors = tf_idf_vectors
        self._full_vocab = full_vocab

    def get_idf(self) -> File:
        return self._idf_dict
    
    def get_tf_idf_vectors(self) -> File:
        return self._tf_idf_vectors
    
    def get_full_vocab(self) -> File:
        return self._full_vocab
