import argparse
from src.user_interfaces.cli import CLI
from src.user_interfaces.gui import GUI

from src.refacto.tf_idf.tf_idf_command import TfIdfCommand
from src.embeddings.embedding_dependencies_handler import EmbeddingDependenciesHandler
from src.refacto.tf_idf.tf_idf_dependencies_handler import TfIdfDependenciesHandler

def main():
    command = TfIdfCommand("dummy", "dummy", "dummy")
    for commandHandler in [TfIdfDependenciesHandler(), EmbeddingDependenciesHandler()]:
        commandHandler.handle(command)

if __name__ == "__main__":
    main()
