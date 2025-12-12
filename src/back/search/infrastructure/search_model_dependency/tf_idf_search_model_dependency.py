from src.back.search.application.ports.search.search_model_dependency import SearchModelDependency
from src.back.search.application.ports.persistence.file import File

class TfIdfSearchModelDependency(SearchModelDependency):

    def __init__(self, idf_dict:File, tf_idf_vectors:File, full_vocab:File):
        self._idf_dict = idf_dict
        self._tf_idf_vectors = tf_idf_vectors
        self._full_vocab = full_vocab

    def get_idf(self) -> File:
        return self._idf_dict
    
    def get_tf_idf_vectors(self) -> File:
        return self._tf_idf_vectors
    
    def get_full_vocab(self) -> File:
        return self._full_vocab
