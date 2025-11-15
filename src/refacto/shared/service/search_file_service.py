from .file_factory import FileFactory

class SearchFileService:

    def __init__(self, search_model_name: str, preprocessor_name: str,):
        self.preprocessor_name = preprocessor_name
        self.search_model_name = search_model_name
        self._file_factory = FileFactory()
    
    #Common
    def get_corpus_files(self): return self._file_factory.create_files_from_corpus()

    #TF-IDF
    def get_index(self): return self._use_factory("index.json")
    def get_inverse_index(self): return self._use_factory("inverse_index.json")
    def get_full_vocab(self): return self._use_factory("full_vocab.json")

    def get_tf(self): return self._use_factory("tf.json")
    def get_idf(self): return self._use_factory("idf.json")
    def get_tf_idf(self): return self._use_factory("tf_idf.json")
    def get_tf_idf_vectors(self): return self._use_factory("tf_idf_vectors.json")

    #Embeddings
    def get_preprocessed_corpus(self): return self._use_factory("preprocessed_merged_corpus.txt")
    def get_fassttext_model(self): return self._use_factory("fasttext_wiki_model.bin")
    def get_documents_embeddings(self): return self._use_factory("fasttext_doc_embeddings.json")


    def _use_factory(self, filename: str):
        return self._file_factory.create(self.search_model_name, self.preprocessor_name, filename)


    

    