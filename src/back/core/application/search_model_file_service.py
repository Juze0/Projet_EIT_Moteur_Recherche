from src.back.core.application.ports.file_factory import FileFactory
from src.back.core.application.ports.paths_provider import PathsProvider


class SearchModelFileService:

    def __init__(self, file_factory: FileFactory, paths_provider: PathsProvider, search_model_name: str, preprocessor_name: str):
        self._file_factory = file_factory
        self._paths_provider = paths_provider
        self._base_path = self._paths_provider.output_dir() / search_model_name / preprocessor_name
    

    def create_corpus_file(self):
        return self._file_factory.create_files_from_folder(self._paths_provider.wiki_corpus_dir())

    #TF-IDF
    def get_index(self): return self.create_file("index.json")
    def get_inverse_index(self): return self.create_file("inverse_index.json")
    def get_full_vocab(self): return self.create_file("full_vocab.json")

    def get_tf(self): return self.create_file("tf.json")
    def get_idf(self): return self.create_file("idf.json")
    def get_tf_idf(self): return self.create_file("tf_idf.json")
    def get_tf_idf_vectors(self): return self.create_file("tf_idf_vectors.json")

    #Embeddings
    def get_preprocessed_corpus(self): return self.create_file("preprocessed_merged_corpus.txt")
    def get_fassttext_model(self): return self.create_file("fasttext_wiki_model.bin")
    def get_documents_embeddings(self): return self.create_file("fasttext_doc_embeddings.json")


    def create_file(self, filename: str):
        return self._file_factory.create_file(self._base_path / filename)
