import os
import math
import json
from collections import defaultdict
# file hierarchy
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum

# Model
from src.search_models.tf_idf.tf_idf_search_model import TFIDFSearchModel
from src.search_models.we_fasttext.embedding_search_model import EmbeddingSearchModel


class Test:
    """Classe s'occupant d'effectuer les tests sur les modèles"""
    
    def __init__(self, model_to_test):
        self.model_to_test = model_to_test

    def set_model_to_test(self, model_to_test):
        self.model_to_test = model_to_test

    ############################# METRICS
    
    def precision_rappel(self, rel, res) :
        r_n_r = [doc for doc in rel if doc in res]
        precision = 0
        rappel = 0
        if len(res) != 0 :
            precision = len(r_n_r) / len(res)
        if len(rel) != 0 :
            rappel = len(r_n_r) / len(rel)
        return precision, rappel

    def Fmesure_1_2_05(self, precision,rappel):
        '''
        F-mesure : 
            0 : plus mauvaise valeur
            1 : meilleure valeur possible
        '''
        F_mesure_1 = 0
        F_mesure_2 = 0
        F_mesure_05 = 0
        if precision + rappel != 0 :
            F_mesure_1 = 2 * precision * rappel / (precision + rappel)
            #plus d'improtance au rappel
            B = 2
            F_mesure_2 = (1+B*B) * precision * rappel / (B*B*precision + rappel)
            
            #plus d'improtance à la precision
            B = 0.5
            F_mesure_05 = (1+B*B) * precision * rappel / (B*B*precision + rappel)
        return F_mesure_1, F_mesure_2, F_mesure_05 

    def AP(self, rel, res):
        if len(rel) == 0 or len(res) == 0:
            return 0
        nbDocCorrect = 0
        sum_precision = 0
        precision_at_k = []  # Pour stocker la précision à chaque point pertinent récupéré
        recall_at_k = []     # Pour stocker le rappel à chaque point pertinent récupéré
        for i, doc in enumerate(res):
            if doc in rel:
                nbDocCorrect += 1
                precision_i = nbDocCorrect / (i + 1)
                sum_precision += precision_i
                # Enregistrement de la précision et du rappel à ce point
                precision_at_k.append(precision_i)
                recall_at_k.append(nbDocCorrect / len(rel))

        return (sum_precision / len(rel) if nbDocCorrect > 0 else 0)#,precision_at_k, recall_at_k

    def PertinanceGradue(self, pertinance):
        p = [int(val / 25) for val in pertinance]
        return p

    def DCG(self, res, pertinance):
        if len(res) != len(pertinance):
            raise ValueError("Les listes 'res' et 'pertinance' doivent avoir la même longueur.")
        pg = self.PertinanceGradue(pertinance)  
        sum_ = 0
        for i in range(len(res)):
            utilite = 2**pg[i] - 1
            pu = 1 / math.log2(i + 2)  # On commence à 2 pour éviter log2(1) qui serait infini
            sum_ += utilite * pu


        return sum_

    def evaluation(self, query, res, rel, pertinance, file_path, remplacer=False):
        # Initialisation des données pour l'entrée
        data_entry = {
            "query": query,
            "relevant_documents": rel,
            "retrieved_documents": res,
            "pertinance": pertinance,
            "metrics": {
                "precision": self.precision_rappel(rel, res)[0],
                "recall": self.precision_rappel(rel, res)[1],
                "F_measure_1": self.Fmesure_1_2_05(*self.precision_rappel(rel, res))[0],
                "F_measure_2": self.Fmesure_1_2_05(*self.precision_rappel(rel, res))[1],
                "F_measure_0.5": self.Fmesure_1_2_05(*self.precision_rappel(rel, res))[2],
                "AP": self.AP(rel, res),#[0],
                "DCG": self.DCG(res, pertinance)
            }
        }

        # Charger le contenu existant et vérifier si la requête existe
        entries = []
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                for line in file:
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue  # Ignore les lignes mal formatées

        # Vérifier si la requête existe déjà dans les résultats
        query_exists = any(entry['query'] == query for entry in entries)
        if query_exists and not remplacer:
            #print(f"Les résultats pour la requête '{query}' existent déjà dans '{file_path}'. Aucun calcul effectué.")
            return  # Si la requête existe et remplacer est False, ne pas refaire les calculs

        # Si la requête existe et que remplacer est True, filtrer l'ancienne entrée
        if query_exists:
            entries = [entry for entry in entries if entry['query'] != query]
            #print(f"Les résultats pour la requête '{query}' seront remplacés.")

        # Ajouter la nouvelle entrée aux résultats
        entries.append(data_entry)

        # Écrire chaque entrée en JSONL dans le fichier
        with open(file_path, "w") as file:
            for entry in entries:
                file.write(json.dumps(entry) + "\n")

        #print(f"Les résultats pour la requête '{query}' ont été ajoutés à '{file_path}'.")

    ############################# I) Calcul en parallèlle des écritures sur le disque
    # Définir le chemin du fichier JSONL

    def regrouper_fichiers_par_question(self):
        """
        Charge les données à partir d'un fichier JSONL et regroupe les fichiers en fonction des questions.
        """
        file_path_requete = FileHierarchyEnum.get_file_path(FileHierarchyEnum.CORRECTION_FOLDER)
        question_to_files = defaultdict(list)
        try:
            with open(file_path_requete, "r") as file:
                for line in file:
                    try:
                        entry = json.loads(line)  # Charger chaque ligne comme un dictionnaire
                        answer_file = entry["Answer file"]
                        for question in entry["Queries"]:  # Boucler sur les requêtes dans 'Queries'
                            question_to_files[question].append(answer_file)
                    except json.JSONDecodeError:
                        print("Ligne mal formée ignorée.")
        except FileNotFoundError:
            print(f"Le fichier '{file_path_requete}' est introuvable.")
        
        return dict(question_to_files)

    def launch_modele_evaluation(self, output_file, lenghthMAX):  #injection de dépendance sur le model !
        question_to_files = self.regrouper_fichiers_par_question()
        for query, files in question_to_files.items():
            print(query)
            #fichiers attendu : 
            rel = files
            #fichiers trouver par le modele : (+pertinance compris entre 0 et 100)
            res = []
            pertinance = []
            #
            results = {}
            results = self.model_to_test.calculate_docs_to_answer_query_docs(query)
            for i, result in enumerate(results.keys()):
                if i < lenghthMAX and results[result] > 0:
                    pertinance.append(round(results[result]*100, 2))
                    res.append(result)
            self.evaluation(query, res, rel, pertinance, output_file)

    ############################# II) Lecture des fichiers sur le disque (cf étape I) et résultat de l'évaluation

    def load_evaluation_data(self, file_path):
        """
        Charge les données à partir d'un fichier JSONL.
        """
        data = []
        with open(file_path, "r") as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    data.append(entry)
                except json.JSONDecodeError:
                    print("Ligne mal formée ignorée.")
        return data

    def calculate_map(self, file_path):
        """
        Calcule la Mean Average Precision (MAP) à partir du fichier JSONL d'évaluations.
        """
        # Charger les données du fichier JSONL
        data = self.load_evaluation_data(file_path)
        
        map_score = 0
        q = 0
        for entry in data:
            ap = entry["metrics"]["AP"]
            q += 1
            map_score += ap

        # Calcul du MAP
        if q > 0:
            map_score /= q 
        
        return map_score
            
    def eval_model(self, file_input):
        map_score = self.calculate_map(file_input)
        print(f"Mean Average Precision (MAP): {map_score:.4f}")

    ############################# III) évaluation complète
    
    def file_path_to_write_in(self):
        model_class = self.model_to_test.__class__
        prepro_during_eval = self.model_to_test.get_model_preprocessor_name()
        if model_class == TFIDFSearchModel:
            return FileHierarchyEnum.get_file_path(FileHierarchyEnum.EVAL_TFIDF, prepro_during_eval)
        if model_class == EmbeddingSearchModel:
            return FileHierarchyEnum.get_file_path(FileHierarchyEnum.EVAL_EMBEDDINGS, prepro_during_eval)

    def complete_eval(self):
        eval_file_path = self.file_path_to_write_in()
        self.launch_modele_evaluation(eval_file_path, 10)
        self.eval_model(eval_file_path)