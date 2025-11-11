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
        # 1ere type : VocabAndIndewCalulatore
        self.get_voc_index_map()
        #self.check_and_create_all("le vocabulaire, l'index et l'index inversé", self.get_voc_index_map(), self.preprocessor.name)
        # 2nd type : TfIDF
        #self.check_and_create_all("TF-IDF", self.get_tf_idf_map(), self.preprocessor.name)
        pass


    def get_voc_index_map(self):
        """Retourne une carte associant les types de fichiers aux méthodes de traitement."""
        #### INTERN DEPENDENCIES => HERE THE ORDER MATTERS !!!
        corpus_folder = FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER)
        corpus_files = [File(full_path_file_name) for full_path_file_name in self.file_handler.get_full_path_files_of_folder(corpus_folder)]

        index_voc_calculator = IndexAndVocabCalculator(self.preprocessor)

        index_file = File(self.file_handler.get_file_path(FileHierarchyEnum.INDEX, self.preprocessor.name))
        inverse_index_file = File(self.file_handler.get_file_path(FileHierarchyEnum.INVERSE_INDEX, self.preprocessor.name))

        inverse_index_file.save_json(index_voc_calculator.create_inversed_index(index_file))

        return {
            FileHierarchyEnum.INDEX:            index_voc_calculator.create_index,
            FileHierarchyEnum.INVERSE_INDEX:    index_voc_calculator.create_inversed_index,
            FileHierarchyEnum.FULL_VOCAB:       index_voc_calculator.extract_full_vocab,
        }
    
    def get_tf_idf_map(self):
        """Retourne une carte associant les types de fichiers aux méthodes de traitement."""
        #### INTERN DEPENDENCIES => HERE THE ORDER MATTERS !!!
        tf_idf_calculator = TFIDFCalculator(self.preprocessor.name, self)
        return {
            FileHierarchyEnum.TF:            tf_idf_calculator.calculate_tf,
            FileHierarchyEnum.IDF:           tf_idf_calculator.calculate_idf,
            FileHierarchyEnum.TF_IDF:        tf_idf_calculator.calculate_tf_idf,
            FileHierarchyEnum.TF_IDF_VECTORS:tf_idf_calculator.create_tf_idf_vectors,
        }
