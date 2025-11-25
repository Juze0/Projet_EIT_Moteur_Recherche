import argparse
from src.user_interfaces.cli import CLI
from src.user_interfaces.gui import GUI

from src.refacto.tf_idf.tf_idf_command import TfIdfCommand
from src.refacto.embeddings.embedding_dependency_resolver import EmbeddingDependencyResolver
from src.refacto.tf_idf.tf_idf_dependency_resolver import TfIdfDependencyResolver

from src.refacto.shared.commands.raw_search_command import RawSearchCommand
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor
from src.search_models.tf_idf.tf_idf_search_model import TFIDFSearchModel

from src.refacto.shared.handler.handler import Handler
from src.refacto.shared.handler.enrich_command_handler import EnrichCommandHandler
from src.refacto.shared.handler.dependencies_handler import DependenciesHandler
from src.refacto.shared.handler.search_request_handler import SearchRequestHandler


def main():
    commandFromUi = RawSearchCommand("SpaCy", "tfidf", "mission apollo NASA")

    handler = EnrichCommandHandler()
    handler.setNext(DependenciesHandler()
          ).setNext(SearchRequestHandler())
    print(handler.handle(commandFromUi))
    

if __name__ == "__main__":
    main()
