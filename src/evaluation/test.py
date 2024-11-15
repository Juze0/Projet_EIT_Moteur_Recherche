import os
import json
import src.evaluation.sur_1_test as t1
import src.evaluation.sur_ensemble_test as te
from collections import defaultdict

# Preprocessor
from src.preprocessing.nltk_preprocessor import NLTKPreprocessor
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor
# Model
from src.search_models.tf_idf.tf_idf_search_model import TFIDFSearchModel
from src.search_models.we_fasttext.embedding_search_model import EmbeddingSearchModel

# Définir le chemin du fichier JSONL



def regrouper_fichiers_par_question(file_path_requete):
    """
    Charge les données à partir d'un fichier JSONL et regroupe les fichiers en fonction des questions.
    """
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


preprocessor = SpaCyPreprocessor()
model = EmbeddingSearchModel(preprocessor)
#model = TFIDFSearchModel(preprocessor)

def launch_modele_evaluation(file_output_eval_model, model, lenghthMAX):
    question_to_files = regrouper_fichiers_par_question("requetes.jsonl")
    for query, files in question_to_files.items():
        print(query)
        #fichiers attendu : 
        rel = files
        #fichiers trouver par le modele : (+pertinance compris entre 0 et 100)
        res = []
        pertinance = []
        #
        results = {}
        results = model.calculate_docs_to_answer_query_docs(query)
        for i, result in enumerate(results.keys()):
            if i < lenghthMAX and results[result] > 0:
                pertinance.append(round(results[result]*100, 2))
                res.append(result)

        t1.evaluation(query, res, rel, pertinance, file_output_eval_model)
    

def eval_model(file_input):
    map_score = te.calculate_map(file_input)
    print(f"Mean Average Precision (MAP): {map_score:.4f}")


launch_modele_evaluation("eval_Embedding_L30.jsonl",model, 30)
eval_model("eval_Embedding_L30.jsonl")


#launch_modele_evaluation("eval_TFIDF.jsonl",model, 10)
#eval_model("eval_TFIDF.jsonl")






