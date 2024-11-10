import sys
from os.path import join
from time import time
from io import StringIO

import customtkinter as ctk
from CTkListbox import *
from src.user_interfaces.ui import UI
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum

# Configuration de l'apparence de CustomTkinter
ctk.set_appearance_mode("Dark")  # Options: "Dark", "Light", ou "System"
ctk.set_default_color_theme("blue")  # Couleur d'accentuation

class GUI(ctk.CTk, UI):
    def __init__(self):
        ctk.CTk.__init__(self)
        # Build the UI
        self.configure_main_window()
        self.build_window_first_section()
        self.build_window_second_section()

        # Redirection de la sortie standard vers la TextBox
        self.stdout = StringIO()
        sys.stdout = self.stdout_writer(self.textbox_console)

        UI.__init__(self)

    def run(self):
        """Démarre l'interface graphique."""
        self.mainloop()

    ##################### Configuration de la GUI

    def configure_main_window(self):
        """Configure la fenêtre principale de l'application."""
        self.title("Moteur de Recherche de Documents")
        self.app_width = 1024
        self.app_height = 768
        self.geometry(f"{self.app_width}x{self.app_height}")
        self.resizable(True, True)  # Désactive la possibilité de redimensionner la fenêtre


    def build_window_first_section(self):
        """Met en place toute la partie gauche de l'interface. Cette partie s'occupe de la partie "recherche de documents\""""
        # CONTAINER
        self.top_container = self.create_frame(self)   
        self.top_container.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="nsew")
        # Organisation de la première section
        self.label_instruction = self.create_label(self.top_container, "Veuillez entrer votre requête (puis appuyez sur la touche ⏎) :")
        self.entry_query = self.create_entry(self.top_container, placeholder="Tapez votre requête ici...", event="<Return>", command=self.on_query_entered)
        self.listbox_query_results = self.create_listbox(self.top_container, width=0.4*self.app_width, height=0.28*self.app_height, command=self.show_file_content)
        self.textbox_result_file = self.create_textbox(self.top_container, width=0.3*self.app_width, height=0.3*self.app_height)
        self.textbox_result_file.grid(column=1, row=2, padx=10, pady=(20, 10), sticky="nsew")
        self.label_console_title = self.create_label(self.top_container, "Console de sortie")
        self.textbox_console = self.create_textbox(self.top_container, width=0.72*self.app_width, height=0.5*self.app_height)

        composant_span_to_change = [self.label_instruction, self.entry_query, self.label_console_title, self.textbox_console]
        for composant in composant_span_to_change:
            composant.grid(columnspan=2)


    def build_window_second_section(self):
        # Deuxième section (à droite) : zone d'évaluation
        self.bottom_section = self.create_frame(self)
        self.bottom_section.grid(row=0, column=2, padx=10, pady=(20, 10), sticky="nsew")
        self.evaluation_label = self.create_label(self.bottom_section, "Évaluation")


    def stdout_writer(self, textbox):
        """Retourne une fonction pour rediriger les impressions vers la TextBox."""
        class StdoutRedirector:
            def __init__(self, textbox):
                self.textbox_console = textbox

            def write(self, message):
                # Affiche le message dans la TextBox
                self.textbox_console.insert("end", message)
                self.textbox_console.see("end")  # Fait défiler vers le bas

            def flush(self):
                pass  # Nécessaire pour la compatibilité avec sys.stdout

        return StdoutRedirector(textbox)


    ##################### Méthodes permettant la construction des élements composants la GUI

    def create_frame(self, parent, **pack_options):
        """Crée un cadre (frame) avec les options spécifiées et le place dans le parent donné."""
        frame = ctk.CTkFrame(parent)
        frame.grid(**pack_options)
        return frame

    def create_label(self, parent, text, **label_options):
        """Crée un label avec le texte et les options spécifiés, puis l'attache au parent donné."""
        label = ctk.CTkLabel(parent, text=text, **label_options)
        label.grid()
        return label
    
    def create_entry(self, parent, placeholder="", width=300, event=None, command=None, **entry_options):
        """Crée un champ de saisie (entry) avec un texte de substitution et des options personnalisables."""
        entry = ctk.CTkEntry(parent, width=width, placeholder_text=placeholder, **entry_options)
        entry.grid()
        if event and command:  # Vérifie si un événement et une commande sont fournis
            entry.bind(event, command)
        return entry

    def create_listbox(self, parent, width, height, command=None):
        """Crée une Listbox et la place dans le parent donné."""
        listbox = CTkListbox(parent, command=command, width=width, height=height) 
        listbox.grid(pady=10)
        return listbox
    

    def create_textbox(self, parent, width, height):
        """Crée et retourne une TextBox pour afficher les messages."""
        textbox = ctk.CTkTextbox(parent, width=width, height=height)
        textbox.grid()
        return textbox
    
    ##################### Commandes appelées lors de la génération d'évènements

    def on_query_entered(self, event=None):
        """Lorsque l'utilisateur appuie sur Entrée après avoir entré une requête."""
        query = self.entry_query.get()
        if query.strip():  # Vérifie si la requête n'est pas vide
            # Passe la requête au modèle pour obtenir les résultats
            start_time = time()
            results = self.calculate_docs_to_answer_query_docs(query)
            end_time = time()
            print(f"Requête effectuée : {query} en {end_time - start_time} secondes !\n")
            # Affiche les résultats dans la Listbox
            self.display_results(results)
        else:
            print("Veuillez entrer une requête valide.")

    
    def display_results(self, results):
        """Affiche les résultats sous forme de liste cliquable dans la TextBox."""
        # Efface les anciens résultats
        self.listbox_query_results.delete("0", "end")  # Utilise "0" pour indiquer le début de la Listbox
        
        # Ajoute chaque résultat (nom de fichier) dans la Listbox
        link = join(FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER))
        for i, result in enumerate(results.keys()):
            relevance_score = round(results[result] * 100, 2)
            with open(f"{link}/{result}", "r", encoding="utf-8") as file:
                title = file.readline().strip()
            self.listbox_query_results.insert("end", f"{result}: {title}, {relevance_score}%",)


    def show_file_content(self, event):
        """Affiche le contenu du fichier sélectionné dans la TextBox textbox_result_file."""
        # Récupère l'élément sélectionné dans la liste des résultats
        idx_selection = self.listbox_query_results.curselection()
        
        if idx_selection:
            file_name_and_info = self.listbox_query_results.get(idx_selection)
            file_name = file_name_and_info.split(".txt")[0] + ".txt"
            file_path = join(FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER), file_name)

            # Lecture du contenu du fichier sélectionné
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            self.textbox_result_file.delete(1.0, "end")  # Efface le contenu précédent
            self.textbox_result_file.insert("end", content)
