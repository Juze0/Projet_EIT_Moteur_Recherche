from src.back.search.domain.search_model_name import SearchModelName
from src.back.search.domain.dependency_resolver import DependencyResolver

from src.back.search.embeddings.embedding_dependency_resolver import EmbeddingDependencyResolver
from src.back.search.tf_idf.tf_idf_dependency_resolver import TfIdfDependencyResolver

class DependencyResolverFactory():

    _dependency_resolver_map = {
        "embedding": EmbeddingDependencyResolver,
        "tfidf": TfIdfDependencyResolver
    }

    def get_search_handler(self, search_model_name: SearchModelName) -> DependencyResolver:
        if search_model_name.value not in self._dependency_resolver_map:
            raise ValueError(f"Dependency resolver '{search_model_name.value}' is not recognized by the factory but is known by business rule!")
        return self._dependency_resolver_map[search_model_name.value]()
    