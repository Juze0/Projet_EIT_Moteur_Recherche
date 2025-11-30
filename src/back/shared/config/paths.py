from pathlib import Path

#
#├── /data
#│   ├── /wiki-corpus
#│   ├── /correction
#│   ├── /output


BASE_DIR = Path(__file__).resolve().parents[4]

# First level
DATA_DIR = BASE_DIR / "data"

# Second level
WIKI_CORPUS_DIR = DATA_DIR / "wiki-corpus"
CORRECTION_DIR = DATA_DIR / "correction"
OUTPUT_DIR = DATA_DIR / "output"