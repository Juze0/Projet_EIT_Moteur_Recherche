import json



def load_evaluation_data(file_path):
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

def calculate_map(file_path):
    """
    Calcule la Mean Average Precision (MAP) à partir du fichier JSONL d'évaluations.
    """
    # Charger les données du fichier JSONL
    data = load_evaluation_data(file_path)
    
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


