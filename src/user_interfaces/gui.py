import sys
from os.path import join
from time import time
from io import StringIO

import customtkinter as ctk
from CTkListbox import *
from src.user_interfaces.ui import UI
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.search_models.tf_idf.tf_idf_search_model import TFIDFSearchModel
from src.search_models.we_fasttext.embedding_search_model import EmbeddingSearchModel

# Configuration de l'apparence de CustomTkinter
ctk.set_appearance_mode("System")  # Options: "Dark", "Light", ou "System"
ctk.set_default_color_theme("blue")  # Couleur d'accentuation

class GUI(ctk.CTk, UI):
    def __init__(self):
        ctk.CTk.__init__(self)
        # Build the UI
        self.configure_main_window()
        self.build_interface_first_row()
        self.build_interface_second_row()
        self.build_interface_third_row()

        # Redirection de la sortie standard vers la TextBox
        self.stdout = StringIO()
        sys.stdout = self.stdout_writer(self.textbox_console)

        UI.__init__(self)
        self.build_window_last_section()

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


    def build_interface_first_row(self):
        """Si l'on admet que l'interface est séparée en "lignes". Cette méthode met en place la première """
        row = 0
        column = 0
        columnspan = 3
        # CONTAINER (sur 2 colonnes)
        self.first_row_container = self.create_frame(self)   
        self.first_row_container.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=(5, 5), sticky="nsew")

        # Organisation de la première ligne
        self.label_instruction = self.create_label(self.first_row_container, "Veuillez choisir votre modèle: ")
        self.label_instruction.grid(row=row, column=column, padx=15)
        # Menu déroulant pour le choix du modèle
        self.model_selection_combo = self.create_combo_box(
            parent=self.first_row_container,
            options=["TF-IDF", "Embeddings"],
            command=self.on_model_selected
        )
        self.model_selection_combo.grid(row=row, column=column+1, padx=10)
        # Gestion du mode sombre/obscure
        self.theme_toggle_switch = self.create_toggle_switch(self.first_row_container, "", self.toggle_theme)
        self.theme_toggle_switch.grid(row=row, column=column+2)
        current_mode = ctk.get_appearance_mode()
        self.theme_toggle_switch.configure(text="Sombre" if current_mode == "Light" else "Clair")


    def build_interface_second_row(self):
        """ Si l'on admet que l'interface est séparée en "lignes". Cette méthode met en place la deuxième.
        Cette partie concerne la partie "recherche de documents\""""
        row = 1
        column = 0
        columnspan = 2
        # CONTAINER
        self.first_row_container = self.create_frame(self)   
        self.first_row_container.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=(5, 5), sticky="nsew")
        # 1 ère ligne: Label pour demander la requete de l'utilisateur et l'entrée correspondante
        self.label_instruction = self.create_label(self.first_row_container, "Veuillez entrer votre requête (puis appuyez sur la touche ⏎) :")
        self.entry_query = self.create_entry(self.first_row_container, placeholder="Tapez votre requête ici...", event="<Return>", command=self.on_query_entered)
        self.listbox_query_results = self.create_listbox(self.first_row_container, width=0.4*self.app_width, height=0.28*self.app_height, command=self.show_file_content)
        self.textbox_result_file = self.create_textbox(self.first_row_container, width=0.3*self.app_width, height=0.3*self.app_height)
        self.textbox_result_file.grid(column=1, row=2, padx=10, pady=(10, 10), sticky="nsew")

        composant_span_to_change = [self.label_instruction, self.entry_query]
        for composant in composant_span_to_change:
            composant.grid(columnspan=2)


    def build_interface_third_row(self):
        """Si l'on admet que l'interface est séparée en "lignes". Cette méthode met en place la troisième et dernière ligne.
        Cette partie concerne la mise en place de la console de sortie (les print sont redirigés dans un textbox !)"""
        row = 2     # Les lignes commencent à zéro ...
        column = 0
        columnspan = 2
        # CONTAINER (sur 2 colonnes)
        self.third_row_container = self.create_frame(self)   
        self.third_row_container.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=(10, 10), sticky="nsew")
        # Espace réservé au label et au textbox de la console
        self.label_console_title = self.create_label(self.third_row_container, "Console de sortie")
        self.textbox_console = self.create_textbox(self.third_row_container, width=0.7*self.app_width, height=0.45*self.app_height)
        self.textbox_console.configure(fg_color=self.third_row_container.cget("fg_color"))
        self.textbox_console.grid(padx=20)


    def build_window_last_section(self):
        row = 1
        column = 2
        rowspan = 2
        # CONTAINER
        # Deuxième section (à droite) : zone d'évaluation
        self.bottom_right_section = self.create_frame(self)
        self.bottom_right_section.grid(row=row, column=column,rowspan=rowspan, pady=(5, 5), sticky="nsew")

        self.evaluation_label = self.create_label(self.bottom_right_section, "Consulation des résultats de l'évaluation")
        # Menu déroulant pour le choix du modèle
        try:
            query_map = self.result_test_reader.get_query_line_map()
            options = list(query_map.keys())
        except Exception as e:
            print(f"Erreur lors du fichier d'évaluation : {e}")
            options = ["Aucun options possibles"]

        self.test_query_selection_combo = self.create_combo_box(
            parent=self.bottom_right_section,
            options=options,
            command=self.on_query_evaluation_result
        )
        ################ PARTIE CONCERNANT LE RECEUIL DE L'ENSEMBLE DES INFOS DE L'EVALUATION
        self.evaluation_result_label = self.create_label(self.bottom_right_section, "Le document a retrouver était: ")
        self.create_label(self.bottom_right_section, "").grid(pady=15) # Label vide servant à laisser de l'espace ...

        # Textbox pour les documents réunies par le model
        self.create_label(self.bottom_right_section, "Documents retrouvé(s) par le modèle: ")
        self.evaluation_result_txtbox = self.create_textbox(self.bottom_right_section, 200, 200)

        self.create_label(self.bottom_right_section, "").grid(pady=15) # Label vide servant à laisser de l'espace ...

        # Textbox pour les documents réunies par le model
        self.create_label(self.bottom_right_section, "Métriques: ")
        self.evaluation_metrics_txtbox = self.create_textbox(self.bottom_right_section, 200, 200)
        #self.evaluation_metrics_txtbox.grid(pady=50)
        ################
        # Exemple d'ajout dans la deuxième ligne (build_interface_second_row)
        #self.progress_bar = self.create_progress_bar(self.bottom_right_section, width=0.3*self.app_width)
        #self.progress_bar.grid(padx=10, sticky="nsew")



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
    
    def create_combo_box(self, parent, options, command, width=200):
        """Crée un menu déroulant pour la sélection des modèles."""
        combo_box = ctk.CTkOptionMenu(
            parent, 
            values=options, 
            command=command,
            width=width
        )
        combo_box.grid(pady=10)
        return combo_box
    

    def create_toggle_switch(self, parent, text, command):
        """Crée un toggle switch pour changer entre les modes clair et sombre."""
        toggle_switch = ctk.CTkSwitch(
            master=parent,
            text=text,
            command=command
        )
        toggle_switch.grid()
        return toggle_switch
    
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
    
    def create_progress_bar(self, parent, width=75):
        """Crée et retourne une barre de progression pour afficher l'avancement."""
        progress_bar = ctk.CTkProgressBar(parent, width=width)
        progress_bar.grid(pady=10)
        progress_bar.set(0)  # Initialise la barre de progression à 0%
        return progress_bar

    
    ##################### Commandes appelées lors de la génération d'évènements

    def on_model_selected(self, selected_model):
        """Mise à jour du modèle en fonction de la sélection de l'utilisateur."""
        if selected_model == "TF-IDF":
            self.set_model(TFIDFSearchModel)
            print("Modèle TF-IDF sélectionné.")
        elif selected_model == "Embeddings":
            self.set_model(EmbeddingSearchModel)
            print("Modèle Embeddings sélectionné.")

    def toggle_theme(self):
        """Change le mode d'apparence entre sombre et clair."""
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.theme_toggle_switch.configure(text="Clair" if new_mode == "Dark" else "Sombre")


    def on_query_entered(self, event=None):
        """Lorsque l'utilisateur appuie sur Entrée après avoir entré une requête."""
        query = self.entry_query.get()
        if query.strip():  # Vérifie si la requête n'est pas vide
            # Passe la requête au modèle pour obtenir les résultats
            start_time = time()
            results = self.calculate_docs_to_answer_query_docs(query)
            end_time = time()
            print(f"Requête effectuée : {query} en {round(end_time - start_time, 2)} secondes !\n")
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

    def on_query_evaluation_result(self, selected_query):
        """
        Gère l'événement de sélection dans la ComboBox des requêtes.
        Met à jour les labels et textboxes avec les informations d'évaluation associées.
        
        :param selected_query: La requête sélectionnée dans la ComboBox.
        """
        try:
            # Vérifie si une requête a été sélectionnée
            if not selected_query or selected_query == "Aucune option possible":
                print("Aucune requête sélectionnée ou options non disponibles.")
                return

            # Récupère le dictionnaire des requêtes et le numéro de ligne associé
            query_map = self.result_test_reader.get_query_line_map()
            if selected_query not in query_map:
                print(f"Requête '{selected_query}' non trouvée.")
                return

            # Récupère les informations associées à la requête
            line_number = query_map[selected_query]
            relevant_doc, retrieved_docs, metrics = self.result_test_reader.extract_query_eval_info(line_number)

            # Mise à jour du label pour le document pertinent
            self.evaluation_result_label.configure(
                text=f"Le document à retrouver était:\n{relevant_doc}"
            )

            # Mise à jour de la textbox pour les documents retrouvés
            self.evaluation_result_txtbox.delete("1.0", "end")
            self.evaluation_result_txtbox.insert("1.0", "\n".join(retrieved_docs))

            # Mise à jour de la textbox pour les métriques
            self.evaluation_metrics_txtbox.delete("1.0", "end")
            for key, value in metrics.items():
                self.evaluation_metrics_txtbox.insert('end', f"{key}: {value:.4f}\n")

        except Exception as e:
            print(f"Erreur lors de la récupération des résultats d'évaluation : {e}")

