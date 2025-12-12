from src.back.search.infrastructure.search_model_dependency_resolver.search_model_dependency_resolver import SearchModelDependencyResolver
from src.back.preprocessor.domain.preprocessor import Preprocessor
from src.back.search.shared.service.search_file_service import SearchFileService
from src.back.search.tf_idf.calculators.tf_idf_calculator import TFIDFCalculator
from src.back.search.tf_idf.calculators.index_vocab_calculator import IndexAndVocabCalculator


class TfIdfDependencyResolver(SearchModelDependencyResolver):

    def __init__(self, preprocessor: Preprocessor, search_file_service: SearchFileService):
        super().__init__(preprocessor, search_file_service)


    def resolve_dependencies(self):
        self.resolve_index_inversed_index_and_full_vocab()
        self.resolve_tf_idf_and_its_vectors()


    def resolve_index_inversed_index_and_full_vocab(self):
        print(f"\n#####  Vérification des prérequis pour utiliser le vocabulaire, l'index et l'index inversé")
        index_voc_calculator = IndexAndVocabCalculator()

        corpus_files = self._search_file_service.get_corpus_files()
        index_file = self._search_file_service.get_index()
        inverse_index_file = self._search_file_service.get_inverse_index()
        full_vocab_file = self._search_file_service.get_full_vocab()

        self.if_file_not_found_launch_calculation(index_file, index_voc_calculator.create_index, self._preprocessor, corpus_files)
        self.if_file_not_found_launch_calculation(inverse_index_file, index_voc_calculator.create_inversed_index, index_file)
        self.if_file_not_found_launch_calculation(full_vocab_file, index_voc_calculator.extract_full_vocab, self._preprocessor, corpus_files)
        print()
    
    def resolve_tf_idf_and_its_vectors(self):
        print(f"\n#####  Vérification des prérequis pour utiliser tf-idf")
        tf_idf_calculator = TFIDFCalculator()

        index_file = self._search_file_service.get_index()
        inverse_index_file = self._search_file_service.get_inverse_index()
        full_vocab_file = self._search_file_service.get_full_vocab()

        tf_file = self._search_file_service.get_tf()
        idf_file = self._search_file_service.get_idf()
        tf_idf_file = self._search_file_service.get_tf_idf()
        tf_idf_vectors_file = self._search_file_service.get_tf_idf_vectors()

        self.if_file_not_found_launch_calculation(tf_file, tf_idf_calculator.calculate_tf, index_file)
        self.if_file_not_found_launch_calculation(idf_file, tf_idf_calculator.calculate_idf, inverse_index_file)
        self.if_file_not_found_launch_calculation(tf_idf_file, tf_idf_calculator.calculate_tf_idf, tf_file, idf_file)
        self.if_file_not_found_launch_calculation(tf_idf_vectors_file, tf_idf_calculator.create_tf_idf_vectors, tf_idf_file, full_vocab_file)
        print()
