import emoji
from rich.console import Console
from rich.table import Table
from rich.text import Text

# File hierarchy
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
# Preprocessor
from src.preprocessing.nltk_preprocessor import NLTKPreprocessor
from src.preprocessing.spacy_preprocessor import SpaCyPreprocessor
# Model
from src.search_models.tf_idf.tf_idf_search_model import TFIDFSearchModel
from src.search_models.we_fasttext.embedding_search_model import EmbeddingSearchModel

def choose_model(preprocessor):
    print("\nVeuillez choisir le modèle de recherche :")
    print("1. TF-IDF")
    print("2. Embedding")
    model_choice = input("Entrez le numéro du modèle: ")
    if model_choice == "1":
        return TFIDFSearchModel(preprocessor)
    elif model_choice == "2":
        return EmbeddingSearchModel(preprocessor)
    else:
        print("Choix invalide, veuillez réessayer.")
        return choose_model()

# Test the normalize method
link = FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER) # Cette mission est à déléguer à un document retriever !!!!
preprocessor = SpaCyPreprocessor()
model = choose_model(preprocessor)
console = Console()


console.print(Text("Bonjour et bienvenue sur votre moteur de recherche de documents !\n", style="bold blue"))
console.print(Text.assemble("Test de la recherche avec", Text(" le modèle de votre choix (tf-idf ou embeddings) \n", style="bold red")))

print("Chargement des fichiers pour la recherche avec tf-idf en cours ...\n")

while True:

    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Document", style="dim", width=12, justify="center", no_wrap=True)
    table.add_column("Pourcentage de pertinence par rapport à la requête", style="dim", width=12, justify="center", no_wrap=True)
    
    query = input("Veuillez entrer votre requête: ")
    if query == "stop":
        break
    console.print("Recherche des documents les plus pertinents en cours...\n")
    results = {}
    results = model.calculate_docs_to_answer_query_docs(query)
    
    if len(results.keys()) <= 0:
        print("Aucun document n'a été trouvé pour votre recherche." + emoji.emojize(":neutral_face:"))
        break
    else :
        print("Voici les documents les plus pertinents pour votre recherche")
        for i, result in enumerate(results.keys()):
            open_doc = open(link + "/" + result, "r", encoding="utf-8")
            title = open_doc.readline() #Récupération du titre du document depuis le dossier de documents bruts
            open_doc.close()
            if i < 10 and results[result] > 0:
                relevance_doc_i = round(results[result]*100, 2)
                table.add_row(result + ": " + title, str(relevance_doc_i) + "%", style="white")
        console.print(table)
    
    change_model = input("\nSouhaitez-vous changer de modèle ? (o/n) : ")
    if change_model.lower() == "o":
        model = choose_model(preprocessor)
