import argparse
from src.user_interfaces.cli import CLI
from src.user_interfaces.gui import GUI

from src.refacto.tf_idf.tf_idf_command import TfIdfCommand
from src.refacto.embeddings.embedding_dependencies_handler import EmbeddingDependenciesHandler
from src.refacto.tf_idf.tf_idf_dependencies_handler import TfIdfDependenciesHandler

from src.refacto.shared.commands.raw_search_command import RawSearchCommand
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor
from src.search_models.tf_idf.tf_idf_search_model import TFIDFSearchModel

def main():
    command = RawSearchCommand("Voici mon prepro", "Voici mon model", "query")
    print(command.get_preprocessor())
    print(command.get_search_model())
    print(command.get_query())

if __name__ == "__main__":
    main()
