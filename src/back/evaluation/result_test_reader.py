import json

class ResultTestReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def set_file_path(self, file_path):
        self.file_path = file_path

    def get_query_line_map(self, key="query"):
        """Charge les requetes depuis le fichier JSONL en fonction retourne un dictionnaire [ req1: numero_ligne ]."""
        options = {}
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file):
                    try:
                        data = json.loads(line.strip())
                        if key in data:
                            options[data[key]] = line_number
                    except json.JSONDecodeError as e:
                        print(f"Erreur JSON à la ligne {line_number}: {e}")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier JSONL : {e}")
        
        return options
    
    def extract_query_eval_info(self, line_number):
        """Lit une ligne du fichier d'évaluation et renvoi le tuple suivant revelant_doc:string, retrieved_docs:list(str), metrics:list(str)."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                # Lire toutes les lignes du fichier
                lines = file.readlines()
                
                # Vérifier que le numéro de ligne est valide
                if line_number < 0 or line_number >= len(lines):
                    raise IndexError("Le numéro de ligne est hors limites.")
                
                # Charger les données JSON de la ligne spécifiée
                data = json.loads(lines[line_number].strip())
                
                # Récupération des informations du documents
                relevant_doc = data.get("relevant_documents", [])
                retrieved_docs = data.get("retrieved_documents", [])
                pertinence_scores = data.get("pertinance", [])
                metrics = data.get("metrics", [])
                
                if len(retrieved_docs) != len(pertinence_scores):
                    raise ValueError("La longueur des documents récupérés et des scores de pertinence ne correspond pas.")
                
                # Construire la liste fusionnée
                retrieved_docs_and_pertinance_scores = [f"{doc} - {score}" for doc, score in zip(retrieved_docs, pertinence_scores)]
                return relevant_doc, retrieved_docs_and_pertinance_scores, metrics

        except Exception as e:
            print(f"Erreur lors de la récupération des informations : {e}")
            return []