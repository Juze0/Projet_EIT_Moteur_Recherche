from enum import Enum
from os.path import join

class FileHierarchyEnum(Enum):
    """
    S'occupe de la gestion des chemins de fichiers du projet.

    ├── /data
    │   ├── /wiki-corpus
    │   ├── /output
    |   │   ├── /tf_idf
    |   │   |   ├── /json
    |   │   ├── /word_embeddings
    |   │   |   ├── /text
    |   │   |   ├── /json
    """
    
    # Dossiers principaux
    DATA_FOLDER = "data"
    OUTPUT_FOLDER = "output"
    
    # Sous-dossiers
    WIKI_CORPUS_FOLDER = "wiki-corpus"
    TF_IDF_FOLDER = "tf_idf"
    WORD_EMBEDDINGS_FOLDER = "word_embeddings"
    JSON_FOLDER = "json"
    TEXT_FOLDER = "text"

    ############## Fichiers spécifiques
    ####### TF-IDF JSON files
    INDEX = "index"
    INVERSE_INDEX = "inverse_index"
    FULL_VOCAB = "full_vocab"
    TF = "tf"
    IDF = "idf"
    TF_IDF = "tf_idf"
    TF_IDF_VECTORS = "tf_idf_vectors"
    WORD_COUNT = "word_count"

    ####### Others files


    @staticmethod
    def valid_filename_enum(filename_enum):
        """
        Vérifie si l'argument donné est une instance valide de FileHierarchyEnum.
        """
        return isinstance(filename_enum, FileHierarchyEnum)
    

    @staticmethod
    def get_tf_idf_authorized_files():
        # Catégories de fichiers pour faciliter le regroupement
        return {FileHierarchyEnum.INDEX, FileHierarchyEnum.INVERSE_INDEX, FileHierarchyEnum.FULL_VOCAB,
                FileHierarchyEnum.TF, FileHierarchyEnum.IDF, FileHierarchyEnum.TF_IDF, FileHierarchyEnum.TF_IDF_VECTORS,
                FileHierarchyEnum.WORD_COUNT}

    @staticmethod
    def get_file_path(filename_enum, filename_suffix=""):
        """
        Renvoie le chemin complet vers le fichier correspondant à l'énumération donnée.
        """
        if not FileHierarchyEnum.valid_filename_enum(filename_enum):
            raise ValueError(f"[ERROR FILE HIERARCHY ENUM]{filename_enum} must be an instance of FileHierarchyEnum")

        # READ OPERATIONS
        if filename_enum == FileHierarchyEnum.WIKI_CORPUS_FOLDER:
            return join(FileHierarchyEnum.DATA_FOLDER.value, FileHierarchyEnum.WIKI_CORPUS_FOLDER.value)

        # WRITE OPERATIONS (or read on a file that had been obtained before through calcul) => OUTPUT FOLDER      
        base_path = join(FileHierarchyEnum.DATA_FOLDER.value, FileHierarchyEnum.OUTPUT_FOLDER.value)  # data/output

        if filename_enum in FileHierarchyEnum.get_tf_idf_authorized_files():
            complete_filename = f"{filename_enum.value}_{filename_suffix}.json" if filename_suffix != "" else f"{filename_enum.value}.json"
            return join(base_path, FileHierarchyEnum.TF_IDF_FOLDER.value, FileHierarchyEnum.JSON_FOLDER.value, complete_filename)
        else:
            raise ValueError(f"[ERROR FILE HIERARCHY ENUM] {filename_enum} is an invalid file enum for path generation")
