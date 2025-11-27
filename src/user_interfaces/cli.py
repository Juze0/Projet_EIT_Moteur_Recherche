from emoji import emojize
from rich.console import Console
from rich.table import Table
from rich.text import Text

from .ui import UI
from src.refacto.front.services.search_ui_service import SearchUiService

class CLI(UI):
    """Class to manage CLI interactions for the document search engine."""
    
    def __init__(self, search_ui_service: SearchUiService):
        super().__init__(search_ui_service)
        self.console = Console()
        self.commands = {
            "H":("Affiche cette aide", self.display_help),
            "P":("Change le préprocesseur actuel (NLTK ou SpaCy)", self.choose_preprocessor),
            "M":("Change le modèle de recherche actuel (TF-IDF ou Embedding)", self.choose_model),
            "E":("Lance une évaluation sur le modèle actuel !", self.start_evaluation),
            "Q":("Arrête l'application", None)
        }


    def run(self):
        """Runs the CLI interface."""
        self.display_intro()
        self.search_and_display_results()


    def display_help(self):
        """Displays available commands to the user."""
        self.console.print("\n[bold green]Commandes disponibles :[/bold green]")
        help_table = Table(show_header=True, header_style="bold magenta")
        help_table.add_column("Commande", style="bold cyan", width=20)
        help_table.add_column("Description", style="white", width=60)
        for command, (description, _) in self.commands.items():
            help_table.add_row(command, description)
        self.console.print(help_table)

    def choose_preprocessor(self):
        """Allows the user to select the text preprocessor."""
        self.console.print("\nVeuillez choisir le préprocesseur de texte :")
        self.console.print("1. NLTK")
        self.console.print("2. SpaCy")
        prepro_choice = input("Entrez le numéro du préprocesseur: ")
        if prepro_choice == "1":
            self._search_ui_service.change_preprocessor("nltk")
        elif prepro_choice == "2":
            self._search_ui_service.change_preprocessor("spacy")
        else:
            self.console.print("Choix invalide, veuillez réessayer.")
            self.choose_preprocessor()

    def choose_model(self):
        """Allows the user to select the search model."""
        self.console.print("\nVeuillez choisir le modèle de recherche :")
        self.console.print("1. TF-IDF")
        self.console.print("2. Embedding")
        model_choice = input("Entrez le numéro du modèle: ")
        if model_choice == "1":
            self._search_ui_service.change_model("tfidf")
        elif model_choice == "2":
            self._search_ui_service.change_model("embedding")
        else:
            self.console.print("Choix invalide, veuillez réessayer.")
            self.choose_model()

    ################################## Affichage dans la CLI

    def display_intro(self):
        """Displays the introductory message."""
        self.console.print(Text("\n\nBonjour et bienvenue sur votre moteur de recherche de documents !\n", style="bold blue"))
        self.console.print(Text.assemble("Test de la recherche avec", Text(" le modèle de votre choix (tf-idf ou embeddings) \n", style="bold red")))
        self.display_help()  # Display help at the start

    def search_and_display_results(self):
        """Prompts user for a query and displays search results."""
        link = None #TODO FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER)
        
        while True:
            query = input("Veuillez entrer votre requête (ou tapez 'help' pour voir les commandes disponibles) : ")
            
            # Traitement d'une potentielle commandes
            if query in self.commands:
                if query == "stop":
                    break
                command_description, command_method = self.commands[query]
                command_method()
                continue

            self.console.print("Recherche des documents les plus pertinents en cours...\n")

            # Recherche des documents les + pertinents !
            results = self._search_ui_service.search(query)
            if not results:
                self.console.print("Aucun document n'a été trouvé pour votre recherche." + emojize(":neutral_face:"))
            else:
                self.display_results_table(results, link)

    def display_results_table(self, results, link):
        """Displays the search results in a formatted table."""
        table = Table(show_header=True, header_style="bold magenta", expand=True)
        table.add_column("Document", style="dim", width=12, justify="center", no_wrap=True)
        table.add_column("Pourcentage de pertinence par rapport à la requête", style="dim", width=12, justify="center", no_wrap=True)

        for i, result in enumerate(results.keys()):
            if i >= 10:
                break
            relevance_score = round(results[result] * 100, 2)
            with open(f"{link}/{result}", "r", encoding="utf-8") as file:
                title = file.readline().strip()
            table.add_row(f"{result}: {title}", f"{relevance_score}%", style="white")

        self.console.print(table)