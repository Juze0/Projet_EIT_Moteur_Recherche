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
        #TODO Afficher à nouveau le cadre (voir ci-dessus)
        #self.check_and_create_all("le vocabulaire, l'index et l'index inversé", self.get_voc_index_map(), self.preprocessor.name)
        # 2nd type : TfIDF
        #self.check_and_create_all("TF-IDF", self.get_tf_idf_map(), self.preprocessor.name)
        pass

    def if_file_not_found_launch_calculation(self, file: File, calculation_func, *args, **kwargs):
        if file.exists():
            print(f"[INFO] Le fichier {file.get_file_name()} est disponible ! Voici son chemin {file.get_path()}")
            return
        print("-----------------")
        print(f"[CREATION START] Le fichier {file.get_path()} n'existe pas, création en cours...")
        self.file_handler.create_all_missing_folders(file.get_path())
        start_time = time.time()
        data_to_save = calculation_func(*args, **kwargs)
        end_time = time.time()
        print(f"[CREATION END] La création du fichier {file.get_file_name()} s'est terminée en {self.get_creation_duration_time(start_time, end_time)}!")
        if data_to_save is None:
            # TODO changer ce comportement là, la sauvegarde est forcément réaliser par un DependencieHandler
            print(f"[INFO] La sauvegarde du fichier a été déléguée au fichier de calcul correspondant")
        else:
            file.save_json(data_to_save)
        print("-----------------")


    def resolve_index_inversed_index_and_full_vocab(self):
        corpus_files = [File(full_path_file) for full_path_file in self.file_handler.get_full_path_files_of_folder(FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER))]
        index_voc_calculator = IndexAndVocabCalculator(self.preprocessor)

        index_file = File(self.file_handler.get_file_path(FileHierarchyEnum.INDEX, self.preprocessor.name))
        inverse_index_file = File(self.file_handler.get_file_path(FileHierarchyEnum.INVERSE_INDEX, self.preprocessor.name))
        full_vocab_file = File(self.file_handler.get_file_path(FileHierarchyEnum.FULL_VOCAB, self.preprocessor.name))

        self.if_file_not_found_launch_calculation(index_file, index_voc_calculator.create_index, corpus_files)
        self.if_file_not_found_launch_calculation(inverse_index_file, index_voc_calculator.create_inversed_index, index_file)
        self.if_file_not_found_launch_calculation(full_vocab_file, index_voc_calculator.extract_full_vocab, corpus_files)
    
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
