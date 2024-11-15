import math
import os
import json


'''
rel : documents attendu
res : documents trouvés à partir des modeles 
'''

def precision_rappel(rel, res) :
    r_n_r = [doc for doc in rel if doc in res]
    precision = 0
    rappel = 0
    if len(res) != 0 :
        precision = len(r_n_r) / len(res)
    if len(rel) != 0 :
        rappel = len(r_n_r) / len(rel)
    return precision, rappel

def Fmesure_1_2_05(precision,rappel):
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

def AP(rel, res):
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



def PertinanceGradue(pertinance):
    p = [int(val / 25) for val in pertinance]
    return p

def DCG(res, pertinance):
    if len(res) != len(pertinance):
        raise ValueError("Les listes 'res' et 'pertinance' doivent avoir la même longueur.")
    pg = PertinanceGradue(pertinance)  
    sum_ = 0
    for i in range(len(res)):
        utilite = 2**pg[i] - 1
        pu = 1 / math.log2(i + 2)  # On commence à 2 pour éviter log2(1) qui serait infini
        sum_ += utilite * pu


    return sum_


def evaluation(query, res, rel, pertinance, file_path, remplacer=False):
    # Initialisation des données pour l'entrée
    data_entry = {
        "query": query,
        "relevant_documents": rel,
        "retrieved_documents": res,
        "pertinance": pertinance,
        "metrics": {
            "precision": precision_rappel(rel, res)[0],
            "recall": precision_rappel(rel, res)[1],
            "F_measure_1": Fmesure_1_2_05(*precision_rappel(rel, res))[0],
            "F_measure_2": Fmesure_1_2_05(*precision_rappel(rel, res))[1],
            "F_measure_0.5": Fmesure_1_2_05(*precision_rappel(rel, res))[2],
            "AP": AP(rel, res),#[0],
            "DCG": DCG(res, pertinance)
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
