from src.back.shared.config.paths import OUTPUT_DIR, WIKI_CORPUS_DIR
from os import listdir
from os.path import join

from src.back.file_handlers.file import File
from src.back.file_handlers.json_file import JSONFile
from src.back.file_handlers.text_file import TextFile
from src.back.file_handlers.fasttext_file import FasttextFile


class FileFactory:

    def create(self, model: str, preproc: str, filename: str) -> File:
        path = OUTPUT_DIR / model / preproc / filename
        if filename.endswith(".json"):  return JSONFile(str(path))
        if filename.endswith(".bin"):   return FasttextFile(str(path))
        return TextFile(str(path))
    

    def create_files_from_corpus(self):
        return [TextFile(join(WIKI_CORPUS_DIR, filename)) for filename in sorted(listdir(WIKI_CORPUS_DIR))] 
