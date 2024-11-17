from os import listdir
from os.path import exists, join, isfile
import fasttext

from src.search_models.calculator import Calculator
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.file_handlers.text_file_handler import TextFileHandler

class WECalculator(Calculator):

    def __init__(self, preprocessor, model_type, max_docs=None):
        self.check_model_type(model_type)
        self.model = None
        self.model_type = model_type
        self.max_docs = max_docs
        super().__init__(preprocessor, TextFileHandler(), "word embeddings")
        self.load_fasttext_model()

    ### parent method to override
    def get_file_processing_map(self):
        """Retourne une carte associant les types de fichiers aux méthodes de traitement."""
        #### INTERN DEPENDENCIES => HERE THE ORDER MATTERS !!!
        return {
            FileHierarchyEnum.WE_PREPROCESSED_MERGED_CORPUS:self.preprocess_and_merge_texts,
            FileHierarchyEnum.WE_FASTTEXT_MODEL: (self.train_and_save_model, self.model_type)
        }

    def preprocess_and_merge_texts(self):
        """
        Prétraite et fusionne le contenu de tous les fichiers d'un dossier en une seule chaîne.
        
        :param input_folder: Chemin du dossier contenant les fichiers à prétraiter.
        :return: Chaîne contenant le texte prétraité de tous les fichiers, séparé par des retours à la ligne.
        """
        folder_name = FileHierarchyEnum.get_file_path(FileHierarchyEnum.WIKI_CORPUS_FOLDER)
        file_list = sorted(listdir(folder_name))[:self.max_docs] if self.max_docs is not None else sorted(listdir(folder_name))
        # On se met d'accord sur l'ordre (ici alphabétique) et ON UTILISE LE MEME à chaque fois !!!
        
        merged_content = []
        for filename in file_list:
            file_path = join(folder_name, filename)
            if isfile(file_path):
                with open(file_path, "r") as f:
                    content = f.read()
                # Preprocessing part !
                processed_content = self.preprocessor.normalize_text(content)
                merged_content.append(" ".join(processed_content))
                # --
        return "\n".join(merged_content)

    ######## MODEL TRAINING PART (training, save and load operations)

    def check_model_type(self, model_type): 
        if model_type not in ["cbow", "skipgram"]:
            raise ValueError("Le paramètre 'model_type' doit être soit 'cbow' soit 'skipgram'.")


    def get_training_parameters(self):
        return {
                "model": self.model_type,
                "lr": 0.3,
                "epoch": 5,
                "dim": 100,
                "ws": 10
            }

    def train_and_save_model(self):
        preprocessed_text_path = FileHierarchyEnum.get_file_path(FileHierarchyEnum.WE_PREPROCESSED_MERGED_CORPUS, self.preprocessor_name)
        params = self.get_training_parameters()
        print(f"[INFO] Début de l'entraînement du modèle fasstext sur le fichier {preprocessed_text_path}...")
        self.model = fasttext.train_unsupervised(preprocessed_text_path, 
                                                 model=params["model"],
                                                 lr=params["lr"],
                                                 epoch=params["epoch"], 
                                                 dim=params["dim"], 
                                                 ws=params["ws"])
        self.save_fasstext_model()

    def get_model_complete_file_path(self):
        """Chaque calculator dépend de la technique de préprocessing. Et commme dans get_file_processing_map, on a ajouté le type du model,
        on est obligé de le repasser ici en paramètre"""
        return FileHierarchyEnum.get_file_path(FileHierarchyEnum.WE_FASTTEXT_MODEL, f"{self.preprocessor_name}_{self.model_type}") #We keep info about preprocessing and model type used !

    def save_fasstext_model(self):
        model_file_path = self.get_model_complete_file_path()
        self.model.save_model(model_file_path)
        print(f"[SAVE] Le modèle fasttext a été entraîné et est sauvegardé dans {model_file_path}")


    def load_fasttext_model(self):
        model_file_path = self.get_model_complete_file_path()
        if not exists(model_file_path):
            raise ValueError("Le modèle doit être chargé ou entraîné avant de l'utiliser.")
        self.model = fasttext.load_model(model_file_path)
        print(f"[READ] Le modèle fasttext a été chargé depuis {model_file_path}")
    
    
    def find_similar_words(self, word, top_n=10):
        if self.model:
            return self.model.get_nearest_neighbors(word, k=top_n)
        else:
            raise ValueError("Le modèle doit être chargé ou entraîné avant de l'utiliser.")