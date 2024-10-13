# Projet Extraction Infos/Textes : Moteur de recherche dans une base de documents textes issus de Wikipédia

L'objectif de ce projet est de créer un moteur de recherche sur des en-têtes de documents textes issus de Wikipédia.

## Fonctionnalités
Nous avons utilisé diverses techniques pour trouver les documents les plus pertinents par rapport à la requête utilisateur.

- TF-IDF : Cette approche utilse le calcul de la fréquence des mots dans le document (Term Frequency) et la fréquence d'un mot dans tous le corpus (Inverse Document Frequency) pour calculer un score de pertinence (TF * IDF).


## Installation

1. Cloner le projet
2. Créer un environnement virtuel
```bash
python -m venv .venv
```
3. Activer l'environnement virtuel
```bash
source .venv/bin/activate
```
3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Pour utiliser TF/IDF, il faut vérifier si les fichiers tf_idf_spacy_vectors et tf_idf_nltk_vectors sont présents dans le dossier json_files_for_tf_idf. Si ce n'est pas le cas, il faut les importer manuellement en exécutant le script suivant :
```bash
git lfs pull
```

NB : Ne pas oublier d'activer l'envrionnement virtuel à chaque fois que vous travaillez sur le projet.

Si vous installer des dépendances supplémentaires, n'oubliez pas de les ajouter au fichier requirements.txt avec la commande suivante :
```bash
pip freeze > requirements.txt
```
