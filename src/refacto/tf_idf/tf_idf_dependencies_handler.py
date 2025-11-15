from src.refacto.shared.handler.dependencies_handler import DependenciesHandler
from src.refacto.shared.commands.command import Command
from src.refacto.shared.commands.rich_search_command import RichSearchCommand

from src.search_models.tf_idf.tf_idf_calculator import TFIDFCalculator
from src.search_models.tf_idf.index_vocab_calculator import IndexAndVocabCalculator


class TfIdfDependenciesHandler(DependenciesHandler):

    def __init__(self):
        super().__init__()


    def resolve_dependencies(self, command: Command): # TODO mettre une richCOmmand ici
        self.resolve_index_inversed_index_and_full_vocab(command)
        self.resolve_tf_idf_and_its_vectors(command)
        #TODO Afficher à nouveau le cadre (voir ci-dessus): self.check_and_create_all("le vocabulaire, l'index et l'index inversé", self.get_voc_index_map(), command.preprocessor.name)


    def resolve_index_inversed_index_and_full_vocab(self, command: RichSearchCommand):
        print(f"\n#####  Vérification des prérequis pour utiliser le vocabulaire, l'index et l'index inversé")
        index_voc_calculator = IndexAndVocabCalculator()

        service = command.get_search_file_service()
        corpus_files = service.get_corpus_files()
        index_file = service.get_index()
        inverse_index_file = service.get_inverse_index()
        full_vocab_file = service.get_full_vocab()

        self.if_file_not_found_launch_calculation(index_file, index_voc_calculator.create_index, command.preprocessor, corpus_files)
        self.if_file_not_found_launch_calculation(inverse_index_file, index_voc_calculator.create_inversed_index, index_file)
        self.if_file_not_found_launch_calculation(full_vocab_file, index_voc_calculator.extract_full_vocab, command.preprocessor, corpus_files)
        print()
    
    def resolve_tf_idf_and_its_vectors(self, command: RichSearchCommand):
        print(f"\n#####  Vérification des prérequis pour utiliser tf-idf")
        tf_idf_calculator = TFIDFCalculator()

        service = command.get_search_file_service()
        index_file = service.get_index()
        inverse_index_file = service.get_inverse_index()
        full_vocab_file = service.get_full_vocab()

        tf_file = service.get_tf()
        idf_file = service.get_idf()
        tf_idf_file = service.get_tf_idf()
        tf_idf_vectors_file = service.get_tf_idf_vectors()

        self.if_file_not_found_launch_calculation(tf_file, tf_idf_calculator.calculate_tf, index_file)
        self.if_file_not_found_launch_calculation(idf_file, tf_idf_calculator.calculate_idf, inverse_index_file)
        self.if_file_not_found_launch_calculation(tf_idf_file, tf_idf_calculator.calculate_tf_idf, tf_file, idf_file)
        self.if_file_not_found_launch_calculation(tf_idf_vectors_file, tf_idf_calculator.create_tf_idf_vectors, tf_idf_file, full_vocab_file)
        print()
