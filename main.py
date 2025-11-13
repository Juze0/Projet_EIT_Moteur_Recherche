import argparse
from src.user_interfaces.cli import CLI
from src.user_interfaces.gui import GUI

from src.tf_idf.tf_idf_command import TfIdfCommand
from src.embeddings.embedding_dependencies_handler import EmbeddingDependenciesHandler

def main():
    command = TfIdfCommand("dummy", "dummy", "dummy")
    commandHandler = EmbeddingDependenciesHandler()
    commandHandler.handle(command)

if __name__ == "__main__":
    main()
