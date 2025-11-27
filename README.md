# Projet Extraction Infos/Textes : Moteur de recherche dans une base de documents textes issus de Wikipédia

L'objectif de ce projet est de créer un moteur de recherche sur des en-têtes de documents textes issus de Wikipédia.

## Fonctionnalités
Nous avons utilisé diverses techniques pour trouver les documents les plus pertinents par rapport à la requête utilisateur.

- TF-IDF : Cette approche utilse le calcul de la fréquence des mots dans le document (Term Frequency) et la fréquence d'un mot dans tous le corpus (Inverse Document Frequency) pour calculer un score de pertinence (TF * IDF).
- Embeddings: Cette approche utilise un modèle **FastText** que nous avons entraîné de manière non supervisée. À partir de ce modèle, nous avons pu déterminer les embeddings associés à chaque mot, puis calculer un embedding pour chaque fichier du corpus.  
    > **Note :** Le fichier `.bin`, contenant le modèle entraîné, est trop volumineux pour être inclus dans le dépôt. Par conséquent, la première fois que vous utiliserez le projet, le programme réentraînera le modèle automatiquement puis vous pourrez l'utiliser.

*Ces deux techniques peuvent être utilisées de deux façons différentes : l'une avec le préprocesseur SpaCy et l'autre avec NLTK*

- Le programme peut être utilisé via la CLI ou la GUI.
- Enfin, vous avez la possibilité d’évaluer les modèles. 
    > **Note :** Pour une requête, vous aurez accès aux métriques suivantes : précision, rappel,F_measure_1, F_measure_2, F_measure_0.5, AP, DCG. Il faudra explicitement demander une évaluation pour accéder au MAP du modèle.


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

NB : Ne pas oublier d'activer l'envrionnement virtuel à chaque fois que vous travaillez sur le projet.

Si vous installer des dépendances supplémentaires, n'oubliez pas de les ajouter au fichier requirements.txt avec la commande suivante :
```bash
pip freeze > requirements.txt
```

## Utilisation

- Le programme peut s'utiliser de deux facons, via la CLI ou la GUI. Si vous êtes sous Linux et que vous souhaitez utiliser la GUI, il se peut que vous deviez installer tkinter manuellement car il n'est pas inclus par défaut avec Python. Pour l'installer :
```bash
sudo apt-get install python3-tk
```

## Lancement de l'application

L'application peut être lancée en ligne de commande avec plusieurs options. Voici les commandes principales :

### Options de commande

Pour voir toutes les options disponibles, utilisez l'argument ```-h``` ou ```--help``` :
```bash
python main.py -h
```

Lancer en ligne de commande (CLI):
```bash
python main.py -i cli
```

Lancer l'interface graphique (GUI):
```bash
python main.py -i gui
```

## Exploration avancée

### CLi et GUI

Comme mentionné précédemment, vous pouvez utiliser le programme via la CLI ou la GUI :

> **Note :** Il est important de préciser que le programme est capable de recalculer les fichiers manquants et nécessaires à l'utilisation du moteur de recherche. Lorsque cela se produit, c'est-à-dire si vous avez supprimé le dossier `output/td_idf` ou encore `output/word_embeddings`, il est conseillé d'avoir une bonne quantité de RAM, un peu de patience, et **de ne pas lancer la GUI** cela la bloquerait ...


* Un des conséquences de cette approche est qu'il peut y avoir une décorrélation entre le modèle actuel et l'évaluation que vous consultez. Le programme ne relance pas automatiquement les évaluations même lorsque le modèle a changé, car cela peut être coûteux (notamment avec TF-IDF). Si vous le souhaitez, vous pouvez explicitement redemander une évaluation !
  
<div align="center">
  <img src="https://github.com/user-attachments/assets/3169899c-eb14-4476-834d-745223f8c4ca" alt="cli-requete">
  <img src="https://github.com/user-attachments/assets/5a3bbda3-78fd-4257-ab63-f949b10ce621" alt="gui-requete">
</div>

*Figure 1 : Lancer une requête avec le modèle de votre choix*

Désormais, lançons une évaluation pour le modèle basé sur les embeddings utilisant Spacy comme préprocessing. Pour cela, démarrer la cli:
1. Lancer newModel, choisissez Embedding
2. Lancer startEval

<div align="center">
  <img src="https://github.com/user-attachments/assets/ff172ade-af82-4b71-bbb4-151b16e52580" alt="start-embedding-spacy-eval">
</div>

*Figure 2 : Résultat de l'évaluation (ici pour le modèle basé sur les embeddings utilisant Spacy comme préprocessing)*

<div align="center">
  <img src="https://github.com/user-attachments/assets/f0831b2b-1e70-4f2c-8152-52d4d96a7f56" alt="consult-evaluation">
</div>

*Figure 3 : Consulter une évaluation*

> **Note :** On note bien la cohérence entre résultat de la requête et les résultats de l'évaluation
