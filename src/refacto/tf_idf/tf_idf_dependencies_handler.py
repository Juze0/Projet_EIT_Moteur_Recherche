from src.refacto.shared.handler.dependencies_handler import DependenciesHandler
from src.refacto.shared.commands.command import Command
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.search_models.tf_idf.tf_idf_calculator import TFIDFCalculator
from src.search_models.tf_idf.index_vocab_calculator import IndexAndVocabCalculator
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor
from src.file_handlers.text_file import TextFile
from src.file_handlers.json_file import JSONFile


class TfIdfDependenciesHandler(DependenciesHandler):

    def __init__(self):
        super().__init__()


    def resolve_dependencies(self, command: Command):
        self.resolve_index_inversed_index_and_full_vocab(command)
        self.resolve_tf_idf_and_its_vectors(command)
        #TODO Afficher à nouveau le cadre (voir ci-dessus): self.check_and_create_all("le vocabulaire, l'index et l'index inversé", self.get_voc_index_map(), command.preprocessor.name)


    def resolve_index_inversed_index_and_full_vocab(self, command: Command):
        print(f"\n#####  Vérification des prérequis pour utiliser le vocabulaire, l'index et l'index inversé")
        index_voc_calculator = IndexAndVocabCalculator()

        corpus_files = [TextFile(full_path_file) for full_path_file in self.get_full_path_files_of_folder(FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER))]
        index_file = JSONFile(self.get_file_path(FileHierarchyEnum.INDEX, command.preprocessor.name))
        inverse_index_file = JSONFile(self.get_file_path(FileHierarchyEnum.INVERSE_INDEX, command.preprocessor.name))
        full_vocab_file = JSONFile(self.get_file_path(FileHierarchyEnum.FULL_VOCAB, command.preprocessor.name))

        self.if_file_not_found_launch_calculation(index_file, index_voc_calculator.create_index, command.preprocessor, corpus_files)
        self.if_file_not_found_launch_calculation(inverse_index_file, index_voc_calculator.create_inversed_index, index_file)
        self.if_file_not_found_launch_calculation(full_vocab_file, index_voc_calculator.extract_full_vocab, command.preprocessor, corpus_files)
        print()
    
    def resolve_tf_idf_and_its_vectors(self, command: Command):
        print(f"\n#####  Vérification des prérequis pour utiliser tf-idf")
        tf_idf_calculator = TFIDFCalculator()

        index_file = JSONFile(self.get_file_path(FileHierarchyEnum.INDEX, command.preprocessor.name))
        inverse_index_file = JSONFile(self.get_file_path(FileHierarchyEnum.INVERSE_INDEX, command.preprocessor.name))
        full_vocab_file = JSONFile(self.get_file_path(FileHierarchyEnum.FULL_VOCAB, command.preprocessor.name))

        tf_file = JSONFile(self.get_file_path(FileHierarchyEnum.TF, command.preprocessor.name))
        idf_file = JSONFile(self.get_file_path(FileHierarchyEnum.IDF, command.preprocessor.name))
        tf_idf_file = JSONFile(self.get_file_path(FileHierarchyEnum.TF_IDF, command.preprocessor.name))
        tf_idf_vectors_file = JSONFile(self.get_file_path(FileHierarchyEnum.TF_IDF_VECTORS, command.preprocessor.name))

        self.if_file_not_found_launch_calculation(tf_file, tf_idf_calculator.calculate_tf, index_file)
        self.if_file_not_found_launch_calculation(idf_file, tf_idf_calculator.calculate_idf, inverse_index_file)
        self.if_file_not_found_launch_calculation(tf_idf_file, tf_idf_calculator.calculate_tf_idf, tf_file, idf_file)
        self.if_file_not_found_launch_calculation(tf_idf_vectors_file, tf_idf_calculator.create_tf_idf_vectors, tf_idf_file, full_vocab_file)
        print()
