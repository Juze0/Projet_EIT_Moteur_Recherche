import fasttext

from src.search_models.calculator import Calculator
from src.file_handlers.file import File
from src.preprocessing.preprocessor import Preprocessor

class WECalculator(Calculator):

    def __init__(self, model_type, max_docs=None):
        super.__init__()
        self.model_type = model_type
        self.max_docs = max_docs

    def normalize_and_merge_texts(self, preprocessor:Preprocessor, files: list[File]):
        # TODO statuer sur le max_docs
        merged_content = []
        for f in files:
            merged_content.append(" ".join(preprocessor.normalize_text(f.load())))
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

    def train_model(self, preprocessed_merged_corpus: File):
        preprocessed_merged_corpus_path = preprocessed_merged_corpus.get_path()
        params = self.get_training_parameters()
        print(f"[INFO] Début de l'entraînement du modèle fasstext sur le fichier {preprocessed_merged_corpus_path}...")
        return fasttext.train_unsupervised(preprocessed_merged_corpus_path, 
                                                 model=params["model"],
                                                 lr=params["lr"],
                                                 epoch=params["epoch"], 
                                                 dim=params["dim"], 
                                                 ws=params["ws"])
        
    # TODO cette méthode n'a rien à faire ici ...
    def find_similar_words(self, word, top_n=10):
        if self.model:
            return self.model.get_nearest_neighbors(word, k=top_n)
        else:
            raise ValueError("Le modèle doit être chargé ou entraîné avant de l'utiliser.")