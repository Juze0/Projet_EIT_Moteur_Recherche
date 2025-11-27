from src.refacto.shared.search_requirement.search_requirement import SearchRequirement
from src.file_handlers.file import File
from src.search_models.we_fasttext.document_vector_calculator import DocumentVectorCalculator

class EmbeddingSearchRequirement(SearchRequirement):

    def __init__(self, query: str, top_n: int, document_vector_calculator: DocumentVectorCalculator,  document_embeddings:File):
        super().__init__(query, top_n)
        self._document_vector_calculator = document_vector_calculator
        self._document_embeddings = document_embeddings

    def get_document_vector_calculator(self) -> DocumentVectorCalculator:
        return self._document_vector_calculator
    
    def get_document_embeddings(self) -> File:
        return self._document_embeddings