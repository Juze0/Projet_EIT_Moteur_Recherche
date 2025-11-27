import argparse
from src.user_interfaces.cli import CLI
from src.user_interfaces.gui import GUI

from src.refacto.shared.mediator_factory import build_mediator
from src.refacto.shared.controller import Controller
from src.refacto.front.services.search_service import SearchService
from src.refacto.front.state.search_state import SearchState

def main():
    # Configuration de l'argument parser
    parser = argparse.ArgumentParser(description="Choisissez l'interface utilisateur.")
    parser.add_argument(
        "-i", "--interface",
        choices=["cli", "gui"],
        default="cli",
        help="Choisissez l'interface utilisateur : 'cli' pour la ligne de commande ou 'gui' pour l'interface graphique."
    )
    
    args = parser.parse_args()
    
    # Initialisation de l'interface choisie
    search_service = SearchService(Controller(build_mediator()), SearchState())
    if args.interface == "cli":
        interface = CLI(search_service)
    else:
        interface = GUI(search_service)
    
    # Lancement de l'application
    interface.run()

if __name__ == "__main__":
    main()
