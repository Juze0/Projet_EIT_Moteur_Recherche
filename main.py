import Tools
import time
import emoji
import rich 
from rich.console import Console
from rich.table import Table
from rich.text import Text

from Preprocessing.nltk_preprocessor import NLTKPreprocessor
from Preprocessing.spacy_preprocessor import SpaCyPreprocessor

# Test the normalize method
link = "./wiki_split_extract_2k"
tools = Tools.Tools(SpaCyPreprocessor())
console = Console()


console.print(Text("Bonjour et bienvenue sur votre moteur de recherche de documents !\n", style="bold blue"))
console.print(Text.assemble("Test de la recherche avec", Text(" tf-idf \n", style="bold red")))

print("Chargement des fichiers pour la recherche avec tf-idf en cours ...\n")

idf = tools.load_json('./json_files_for_tf_idf/idf_spacy.json')
tf_idf_vectors = tools.load_json('./json_files_for_tf_idf/tf_idf_spacy_vectors.json')

while True:

    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Document", style="dim", width=12, justify="center", no_wrap=True)
    table.add_column("Pourcentage de pertinence par rapport à la requête", style="dim", width=12, justify="center", no_wrap=True)
    
    query = input("Veuillez entrer votre requête: ")
    if query == "stop":
        break
    console.print("Recherche des documents les plus pertinents en cours...\n")
    results = {}
    results = tools.calculate_docs_to_answer_query_docs(query, tf_idf_vectors,idf)
    
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
