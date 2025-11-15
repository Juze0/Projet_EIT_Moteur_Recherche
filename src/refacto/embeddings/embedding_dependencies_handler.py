from src.refacto.shared.handler.dependencies_handler import DependenciesHandler
from src.refacto.shared.commands.command import Command
from src.file_handlers.text_file import TextFile
from src.file_handlers.fasttext_file import FasttextFile
from src.file_handlers.json_file import JSONFile
from src.search_models.we_fasttext.we_calculator import WECalculator
from src.search_models.we_fasttext.document_vector_calculator import DocumentVectorCalculator
from src.refacto.shared.service.search_file_service import SearchFileService
from src.refacto.shared.commands.rich_search_command import RichSearchCommand


class EmbeddingDependenciesHandler(DependenciesHandler):

    def __init__(self):
        super().__init__()


    def resolve_dependencies(self, command: Command): # TODO mettre une richCOmmand ici
        self.resolve_preprocessed_merged_corpus_and_model_training(command)
        self.resolve_documents_embeddings(command)


    def resolve_preprocessed_merged_corpus_and_model_training(self, command: RichSearchCommand):
        """Retourne une carte associant les types de fichiers aux méthodes de traitement."""
        print(f"\n#####  Vérification des prérequis pour utiliser les word embeddings")
        we_calculator = WECalculator("skipgram")

        service = command.get_search_file_service()
        corpus_files = service.get_corpus_files()
        preprocessed_merged_corpus_file = service.get_preprocessed_corpus()
        fasttext_model =service.get_fassttext_model()

        self.if_file_not_found_launch_calculation(preprocessed_merged_corpus_file, we_calculator.build_normalized_corpus, command._preprocessor, corpus_files)
        self.if_file_not_found_launch_calculation(fasttext_model, we_calculator.train_model, preprocessed_merged_corpus_file)
    

    def resolve_documents_embeddings(self, command: RichSearchCommand):
        print(f"\n#####  Vérification des prérequis pour utiliser les embeddings de chaque document du corpus !")
        service = command.get_search_file_service()
        fasttext_model =service.get_fassttext_model()
        document_vector_calculator = DocumentVectorCalculator(fasttext_model)

        corpus_files = service.get_corpus_files()
        preprocessed_merged_corpus_file = service.get_preprocessed_corpus()
        doc_embeddings = service.get_documents_embeddings()


        self.if_file_not_found_launch_calculation(doc_embeddings,
                                                  document_vector_calculator.calculate_embeddings_for_all_documents,
                                                  preprocessed_merged_corpus_file, [f.get_file_name() for f in corpus_files])
        print()