import argparse
from src.user_interfaces.cli import CLI
from src.user_interfaces.gui import GUI

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
    if args.interface == "cli":
        interface = CLI()
    else:
        interface = GUI()
    
    # Lancement de l'application
    interface.run()

if __name__ == "__main__":
    main()
