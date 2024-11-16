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