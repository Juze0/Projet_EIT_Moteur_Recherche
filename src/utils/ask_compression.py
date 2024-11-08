# PYTHONPATH=. python3 ./src/utils/ask_compression.py

from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum

from src.file_handlers.json_file_handler import JSONFileHandler
from src.file_handlers.file_compressor_decorator import FileCompressorDecorator


json_files_path_to_compress = [
    FileHierarchyEnum.get_file_path(FileHierarchyEnum.TF_IDF_VECTORS, "spacy"),
    FileHierarchyEnum.get_file_path(FileHierarchyEnum.TF_IDF_VECTORS, "nltk"),
]

def compress_all_files(file_handler, files_path_to_compress):
    file_compressor = FileCompressorDecorator(file_handler)
    for file_path in files_path_to_compress:
        print("----------------")
        print(f"Traitement de la compression pour le fichier: {file_path}")
        file_compressor.save(file_handler.load(file_path), file_path)
        print("----------------")


def main():
    # 1/3 Déterminer les fichiers à compresser
    # 2/3 Appeller la méthodr avec le file_handler correspondant aux fichiers à compresser
    # 3/3 => OUVRIR UN TERMINAL ET EXECUTER LA COMMANDE SUIVANTE DEPUIS LA RACINE DU PROJET (Projet_EIT_Moteur_Recherche)
    # PYTHONPATH=. python3 ./src/utils/ask_compression.py
    compress_all_files(JSONFileHandler(), json_files_path_to_compress)


if __name__ == "__main__":
    main()