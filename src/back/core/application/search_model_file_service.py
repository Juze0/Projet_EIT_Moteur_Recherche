from src.back.core.application.ports.file_factory import FileFactory
from src.back.core.application.ports.paths_provider import PathsProvider
from src.back.core.application.ports.file import File


class SearchModelFileService: # TODO à renommer: FileRetrieverService et casser la classe ...

    def __init__(self, file_factory: FileFactory, paths_provider: PathsProvider, search_model_name: str, preprocessor_name: str):
        self._file_factory = file_factory
        self._paths_provider = paths_provider
        self._output_path = self._paths_provider.output_dir() / search_model_name / preprocessor_name
    

    def get_corpus_files(self):
        return self._file_factory.get_files_from_folder(self._paths_provider.wiki_corpus_dir())
    

    def get_corpus_subset_files(self, filenames: list[str]) -> dict[str, File]:
        base_path = self._paths_provider.wiki_corpus_dir()
        return {
            filename: self._file_factory.get_file(base_path / filename)
            for filename in filenames
        }
    
    
    def get_output_file(self, filename: str):
        return self._file_factory.get_file(self._output_path / filename)

    #TF-IDF (Définir un object client qui consomme les services de SearchModelService => DI)
    def get_index(self): return self.get_output_file("index.json")
    def get_inverse_index(self): return self.get_output_file("inverse_index.json")
    def get_full_vocab(self): return self.get_output_file("full_vocab.json")

    def get_tf(self): return self.get_output_file("tf.json")
    def get_idf(self): return self.get_output_file("idf.json")
    def get_tf_idf(self): return self.get_output_file("tf_idf.json")
    def get_tf_idf_vectors(self): return self.get_output_file("tf_idf_vectors.json")

    #Embeddings  (Définir un object client qui consomme les services de SearchModelService => DI)
    def get_preprocessed_corpus(self): return self.get_output_file("preprocessed_merged_corpus.txt")
    def get_fassttext_model(self): return self.get_output_file("fasttext_wiki_model.bin")
    def get_documents_embeddings(self): return self.get_output_file("fasttext_doc_embeddings.json")
