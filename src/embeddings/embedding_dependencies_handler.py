from src.shared.handler.dependencies_handler import DependenciesHandler
from src.shared.command import Command
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor
from src.file_handlers.text_file import TextFile
from src.file_handlers.fasttext_file import FasttextFile
from src.file_handlers.json_file import JSONFile
from src.search_models.we_fasttext.we_calculator import WECalculator
from src.search_models.we_fasttext.document_vector_calculator import DocumentVectorCalculator


class EmbeddingDependenciesHandler(DependenciesHandler):

    def __init__(self):
        super().__init__()
        self.preprocessor = SpaCyPreprocessor()


    def handle(self, command: Command):
        self.resolve_dependencies()


    def resolve_dependencies(self):
        self.resolve_preprocessed_merged_corpus_and_model_training()
        self.resolve_documents_embeddings()


    def resolve_preprocessed_merged_corpus_and_model_training(self):
        """Retourne une carte associant les types de fichiers aux méthodes de traitement."""
        print(f"\n#####  Vérification des prérequis pour utiliser les word embeddings")
        we_calculator = WECalculator("skipgram")

        corpus_files = [TextFile(full_path_file) for full_path_file in sorted(self.get_full_path_files_of_folder(FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER)))]

        preprocessed_merged_corpus_file = TextFile(self.get_file_path(FileHierarchyEnum.WE_PREPROCESSED_MERGED_CORPUS, self.preprocessor.name))
        fasttext_model = FasttextFile(self.get_file_path(FileHierarchyEnum.WE_FASTTEXT_MODEL, f"{self.preprocessor.name}_{"skipgram"}"))

        self.if_file_not_found_launch_calculation(preprocessed_merged_corpus_file, we_calculator.build_normalized_corpus, self.preprocessor, corpus_files)
        self.if_file_not_found_launch_calculation(fasttext_model, we_calculator.train_model, preprocessed_merged_corpus_file)
    

    def resolve_documents_embeddings(self):
        print(f"\n#####  Vérification des prérequis pour utiliser les embeddings de chaque document du corpus !")
        document_vector_calculator = DocumentVectorCalculator("skipgram")

        preprocessed_merged_corpus_file = TextFile(self.get_file_path(FileHierarchyEnum.WE_PREPROCESSED_MERGED_CORPUS, self.preprocessor.name))
        fasttext_model = FasttextFile(self.get_file_path(FileHierarchyEnum.WE_FASTTEXT_MODEL, f"{self.preprocessor.name}_{"skipgram"}"))
        doc_embeddings = JSONFile(self.get_file_path(FileHierarchyEnum.WE_FASSTEXT_DOCUMENT_EMBEDDINGS, f"{self.preprocessor.name}_{"skipgram"}"))

        corpus_files = [TextFile(full_path_file) for full_path_file in self.get_full_path_files_of_folder(FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER))]
        ordered_corpus_files = sorted([f.get_file_name() for f in corpus_files])

        self.if_file_not_found_launch_calculation(doc_embeddings,
                                                  document_vector_calculator.calculate_embeddings_for_all_documents,
                                                  fasttext_model, preprocessed_merged_corpus_file, ordered_corpus_files)
        print()