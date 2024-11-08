from abc import ABC, abstractmethod
from os import makedirs, remove
from os.path import exists, join, dirname, getsize
from sys import exit

from .file_hierarchy_enum import FileHierarchyEnum

class FileHandler(ABC):
    """
    Classe générique abstraite dédiée aux opérations de manipulation de fichiers.
    """
    def __init__(self, file_hierarchy_enum=FileHierarchyEnum):
        """
        Initialise le gestionnaire de fichiers avec une classe d'énumération pour la validation des noms de fichiers.
        :param file_hierarchy_enum: Classe d'énumération qui contient les types de fichiers valides.
        """
        self.file_hierarchy_enum = file_hierarchy_enum

    ###### File hierarchy enum based operations
    
    def get_file_path(self, filename_enum, filename_suffix=""):
        """Utilise l'enum décrivant la hierarchie de fichier pour obtenir le chemin du fichier spéicifié !"""
        return self.file_hierarchy_enum.get_file_path(filename_enum, filename_suffix)

    ###### Classic file based operations

    def path_exists(self, file_path):
        """Vérifie si le chemin existe."""
        return exists(file_path)
    
    def get_folder_path(self, file_path):
        """Retourne le chemin du dossier d'un fichier donné."""
        return dirname(file_path)

    def create_all_missing_folders(self, file_path):
        """Crée le dossier s'il n'existe pas."""
        folder_path = self.get_folder_path(file_path)
        makedirs(folder_path, exist_ok=True)

    def get_folder_path(self, file_path):
        """Retourne le chemin du dossier d'un fichier donné."""
        return dirname(file_path)

    def join_paths(self, *paths):
        """Assemble plusieurs chemins en un seul chemin complet."""
        return join(*paths)

    def exit_with_error(self, message):
        """Affiche un message d'erreur et quitte le programme."""
        print(f"[ERROR]: {message}")
        exit(1)

    def path_getsize(self, file_path):
        return getsize(file_path)
    
    def remove_path(self, file_path):
        remove(file_path)

    ###### SAVE AND LOAD OPERATIONS
    ### 1) From the outside, all save and load operations use file_hierarchy_enum
    ### 2) The base classe requires its children to implement both save and load methods

    def save_using_enum(self, data, filename_enum, filename_suffix=""):
        """Utilise l'enum de l'arboresence des fichiers pour savoir où sauvegarder le fichier en paramètre !"""
        file_path = self.get_file_path(filename_enum, filename_suffix)
        self.save(data, file_path)

    @abstractmethod
    def save(self, data, file_path):
        """Méthode abstraite pour enregistrer des données dans un fichier."""
        raise NotImplementedError("This method in not implemented in the subclasses !")

    def load_using_enum(self, filename_enum, file_name_remaining=""):
        """Utilise l'enum de l'arboresence des fichiers pour savoir où charger le fichier en paramètre !"""
        file_path = self.get_file_path(filename_enum, file_name_remaining)
        return self.load(file_path)

    @abstractmethod
    def load(self, file_path):
        """Méthode abstraite pour charger des données depuis un fichier."""
        raise NotImplementedError("This method in not implemented in the subclasses !")

