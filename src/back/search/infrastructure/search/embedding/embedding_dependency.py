from src.back.search.application.ports.output.search.search_model_dependency import SearchModelDependency
from src.back.core.application.ports.file import File
from src.back.search.infrastructure.search.embedding.calculators.document_vector_calculator import DocumentVectorCalculator

class EmbeddingDependency(SearchModelDependency):

    def __init__(self, document_vector_calculator: DocumentVectorCalculator,  document_embeddings:File):
        self._document_vector_calculator = document_vector_calculator
        self._document_embeddings = document_embeddings

    def get_document_vector_calculator(self) -> DocumentVectorCalculator:
        return self._document_vector_calculator
    
    def get_document_embeddings(self) -> File:
        return self._document_embeddings