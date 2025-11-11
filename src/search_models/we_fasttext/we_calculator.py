from os import listdir
from os.path import exists, join, isfile
import fasttext

from src.search_models.calculator import Calculator
from src.file_handlers.file_hierarchy_enum import FileHierarchyEnum
from src.file_handlers.text_file_handler import TextFileHandler
from src.shared.files.file import File

class WECalculator(Calculator):

    def __init__(self, preprocessor, model_type, max_docs=None):
        self.model = None
        self.model_type = model_type
        self.max_docs = max_docs
        super().__init__(preprocessor, TextFileHandler(), "word embeddings")
        self.load_fasttext_model()


    def normalize_and_merge_texts(self, files: list[File]):
        # TODO statuer sur le max_docs
        merged_content = []
        for f in files:
            merged_content.append(" ".join(self.preprocessor.normalize_text(f.load_text_content())))
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

    def train_and_save_model(self, preprocessed_merged_corpus: File):
        preprocessed_merged_corpus_path = preprocessed_merged_corpus.get_path()
        params = self.get_training_parameters()
        print(f"[INFO] Début de l'entraînement du modèle fasstext sur le fichier {preprocessed_merged_corpus_path}...")
        self.model = fasttext.train_unsupervised(preprocessed_merged_corpus_path, 
                                                 model=params["model"],
                                                 lr=params["lr"],
                                                 epoch=params["epoch"], 
                                                 dim=params["dim"], 
                                                 ws=params["ws"])
        self.save_fasstext_model()

    def save_fasstext_model(self, model_file_path: str):
        self.model.save_model(model_file_path)
        print(f"[SAVE] Le modèle fasttext a été entraîné et est sauvegardé dans {model_file_path}")


    def load_fasttext_model(self, model_file_path: str):
        if not exists(model_file_path):
            raise ValueError("Le modèle doit être chargé ou entraîné avant de l'utiliser.")
        self.model = fasttext.load_model(model_file_path)
        print(f"[READ] Le modèle fasttext a été chargé depuis {model_file_path}")
    
    
    def find_similar_words(self, word, top_n=10):
        if self.model:
            return self.model.get_nearest_neighbors(word, k=top_n)
        else:
            raise ValueError("Le modèle doit être chargé ou entraîné avant de l'utiliser.")