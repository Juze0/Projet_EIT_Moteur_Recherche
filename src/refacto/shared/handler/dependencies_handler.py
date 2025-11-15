from src.refacto.shared.handler.handler import Handler
from src.file_handlers.file import File
from src.refacto.shared.commands.command import Command

from abc import abstractmethod

from os import listdir
from os.path import join

class DependenciesHandler(Handler):

    def __init__(self):
        super().__init__()


    def handle(self, command: Command):
        command.get_dependencies_handler().resolve_dependencies(command)
        self._next.handle(command)
    
    #@abstractmethod TODO remettre
    def resolve_dependencies(self, command: Command):
        raise NotImplementedError("This method in not implemented !")

    
    def if_file_not_found_launch_calculation(self, file: File, calculation_func, *args, **kwargs):
        if file.exists():
            print(f"[INFO] Le fichier {file.get_file_name()} est disponible ! Voici son chemin {file.get_path()}")
            return
        print("-----------------")
        print(f"[CREATION START] Le fichier {file.get_path()} n'existe pas, création en cours...")
        file.create_all_missing_folders() # TODO, délégué cette méthode 
        data_to_save = calculation_func(*args, **kwargs)
        if data_to_save is None:
            # TODO changer ce comportement là, la sauvegarde est forcément réaliser par un DependencieHandler
            print(f"[INFO] La sauvegarde du fichier a été déléguée au fichier de calcul correspondant")
        else:
            file.save(data_to_save) # TODO, On addresse désormais ce problème
        print("-----------------")