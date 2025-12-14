from pathlib import Path
from src.back.core.application.ports.paths_provider import PathsProvider

#├── /data
#│   ├── /wiki-corpus
#│   ├── /correction
#│   ├── /output

BASE_DIR = Path(__file__).resolve().parents[4]
DATA_DIR = BASE_DIR / "data"
WIKI_CORPUS_DIR = DATA_DIR / "wiki-corpus"
CORRECTION_DIR = DATA_DIR / "correction"
OUTPUT_DIR = DATA_DIR / "output"

class LocalPathsProvider(PathsProvider):

    def __init__(self):
        self._wiki_dir = WIKI_CORPUS_DIR
        self._correction_dir = CORRECTION_DIR
        self._output_dir = OUTPUT_DIR

    def wiki_corpus_dir(self) -> Path:
        return self._wiki_dir

    def correction_dir(self) -> Path:
        return self._correction_dir
    
    def output_dir(self) -> Path:
        return self._output_dir
