import time

from src.shared.handler.dependencies_handler import DependenciesHandler
from src.shared.command import Command
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.search_models.tf_idf.tf_idf_calculator import TFIDFCalculator
from src.search_models.tf_idf.index_vocab_calculator import IndexAndVocabCalculator
from src.file_handlers.text_file_handler import TextFileHandler
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor
from src.shared.files.file import File
from src.search_models.we_fasttext.we_calculator import WECalculator


class EmbeddingDependenciesHandler(DependenciesHandler):

    def __init__(self):
        super().__init__(TextFileHandler())
        self.preprocessor = SpaCyPreprocessor()


    def handle(self, command: Command):
        self.resolve_dependencies()


    def resolve_dependencies(self):
        self.resolve_index_inversed_index_and_full_vocab()
        self.resolve_tf_idf_and_its_vectors()
        #TODO Afficher à nouveau le cadre (voir ci-dessus): self.check_and_create_all("le vocabulaire, l'index et l'index inversé", self.get_voc_index_map(), self.preprocessor.name)

    ### parent method to override
    def get_file_processing_map(self):
        """Retourne une carte associant les types de fichiers aux méthodes de traitement."""
        we_calculator = WECalculator(self.preprocessor)

        corpus_files = [File(full_path_file) for full_path_file in self.file_handler.get_full_path_files_of_folder(FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER))]
        ordered_corpus_files = sorted([f.get_file_name() for f in corpus_files])

        preprocessed_merged_corpus_file = File(self.file_handler.get_file_path(FileHierarchyEnum.WE_PREPROCESSED_MERGED_CORPUS, self.preprocessor.name))
        fasttext_model = File(self.file_handler.get_file_path(FileHierarchyEnum.WE_FASTTEXT_MODEL, f"{self.preprocessor.name}_{"skipgram"}"))
        # TODO, il faut désromais passer la bonne instance de file à la méthode de calcul

        self.if_file_not_found_launch_calculation(preprocessed_merged_corpus_file, we_calculator.normalize_and_merge_texts, ordered_corpus_files)
        self.if_file_not_found_launch_calculation(fasttext_model, we_calculator.train_and_save_model, preprocessed_merged_corpus_file)
    

    def resolve_index_inversed_index_and_full_vocab(self):
        print(f"\n#####  Vérification des prérequis pour utiliser le vocabulaire, l'index et l'index inversé")
        index_voc_calculator = WECalculator(self.preprocessor)

        corpus_files = [File(full_path_file) for full_path_file in self.file_handler.get_full_path_files_of_folder(FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER))]
        index_file = File(self.file_handler.get_file_path(FileHierarchyEnum.INDEX, self.preprocessor.name))
        inverse_index_file = File(self.file_handler.get_file_path(FileHierarchyEnum.INVERSE_INDEX, self.preprocessor.name))
        full_vocab_file = File(self.file_handler.get_file_path(FileHierarchyEnum.FULL_VOCAB, self.preprocessor.name))

        self.if_file_not_found_launch_calculation(index_file, index_voc_calculator.create_index, corpus_files)
        self.if_file_not_found_launch_calculation(inverse_index_file, index_voc_calculator.create_inversed_index, index_file)
        self.if_file_not_found_launch_calculation(full_vocab_file, index_voc_calculator.extract_full_vocab, corpus_files)
        print()