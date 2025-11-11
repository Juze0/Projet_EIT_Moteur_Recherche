import time

from src.shared.handler.dependencies_handler import DependenciesHandler
from src.shared.command import Command
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.search_models.tf_idf.tf_idf_calculator import TFIDFCalculator
from src.search_models.tf_idf.index_vocab_calculator import IndexAndVocabCalculator
from src.file_handlers.json_file_handler import JSONFileHandler
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor
from src.shared.files.file import File


class TfIdfDependenciesHandler(DependenciesHandler):

    def __init__(self):
        super().__init__(JSONFileHandler())
        self.preprocessor = SpaCyPreprocessor()


    def handle(self, command: Command):
        self.resolve_dependencies()


    def resolve_dependencies(self):
        self.resolve_index_inversed_index_and_full_vocab()
        self.resolve_tf_idf_and_its_vectors()
        #TODO Afficher à nouveau le cadre (voir ci-dessus): self.check_and_create_all("le vocabulaire, l'index et l'index inversé", self.get_voc_index_map(), self.preprocessor.name)


    def resolve_index_inversed_index_and_full_vocab(self):
        print(f"\n#####  Vérification des prérequis pour utiliser le vocabulaire, l'index et l'index inversé")
        index_voc_calculator = IndexAndVocabCalculator(self.preprocessor)

        corpus_files = [File(full_path_file) for full_path_file in self.file_handler.get_full_path_files_of_folder(FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER))]
        index_file = File(self.file_handler.get_file_path(FileHierarchyEnum.INDEX, self.preprocessor.name))
        inverse_index_file = File(self.file_handler.get_file_path(FileHierarchyEnum.INVERSE_INDEX, self.preprocessor.name))
        full_vocab_file = File(self.file_handler.get_file_path(FileHierarchyEnum.FULL_VOCAB, self.preprocessor.name))

        self.if_file_not_found_launch_calculation(index_file, index_voc_calculator.create_index, corpus_files)
        self.if_file_not_found_launch_calculation(inverse_index_file, index_voc_calculator.create_inversed_index, index_file)
        self.if_file_not_found_launch_calculation(full_vocab_file, index_voc_calculator.extract_full_vocab, corpus_files)
        print()
    
    def resolve_tf_idf_and_its_vectors(self):
        print(f"\n#####  Vérification des prérequis pour utiliser tf-idf")
        tf_idf_calculator = TFIDFCalculator(self.preprocessor.name)

        index_file = File(self.file_handler.get_file_path(FileHierarchyEnum.INDEX, self.preprocessor.name))
        inverse_index_file = File(self.file_handler.get_file_path(FileHierarchyEnum.INVERSE_INDEX, self.preprocessor.name))
        full_vocab_file = File(self.file_handler.get_file_path(FileHierarchyEnum.FULL_VOCAB, self.preprocessor.name))

        tf_file = File(self.file_handler.get_file_path(FileHierarchyEnum.TF, self.preprocessor.name))
        idf_file = File(self.file_handler.get_file_path(FileHierarchyEnum.IDF, self.preprocessor.name))
        tf_idf_file = File(self.file_handler.get_file_path(FileHierarchyEnum.TF_IDF, self.preprocessor.name))
        tf_idf_vectors_file = File(self.file_handler.get_file_path(FileHierarchyEnum.TF_IDF_VECTORS, self.preprocessor.name))

        self.if_file_not_found_launch_calculation(tf_file, tf_idf_calculator.calculate_tf, index_file)
        self.if_file_not_found_launch_calculation(idf_file, tf_idf_calculator.calculate_idf, inverse_index_file)
        self.if_file_not_found_launch_calculation(tf_idf_file, tf_idf_calculator.calculate_tf_idf, tf_file, idf_file)
        self.if_file_not_found_launch_calculation(tf_idf_vectors_file, tf_idf_calculator.create_tf_idf_vectors, tf_idf_file, full_vocab_file)
        print()
