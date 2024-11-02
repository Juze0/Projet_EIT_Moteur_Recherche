from sys import exit
from enum import Enum

class JSONFileType(Enum):
    
    ######## FOLDER_NAME
    # wiki-date file folder
    WIKI_FOLDER = "wiki_split_extract_2k"
    # Result file folder
    JSON_FILES_FOLDER = "json_files_for_tf_idf"
    # --- VOCAB
    FULL_VOCAB = "full_vocab"
    # --- INDEX
    INDEX = "index"
    INVERSE_INDEX = "inverse_index"
    # --- STATISTIQUES
    WORD_COUNT = "word_count"
    # --- TF-IDF
    TF = "tf"
    IDF = "idf"
    TF_IDF = "tf_idf"
    TF_IDF_VECTORS = "tf_idf_vectors"

    @staticmethod
    def valid_file_name(file_type):
        """
        Vérifie si l'argument donné est une instance de JSONFileType.
        Si non, affiche une erreur et quitte le programme.
        """
        if isinstance(file_type, JSONFileType):
            return True
        print(f"[ERROR] : '{file_type}' n'est pas un type de fichier JSON valide.")
        exit(1) 