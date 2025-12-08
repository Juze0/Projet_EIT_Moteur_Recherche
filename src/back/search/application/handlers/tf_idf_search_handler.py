from src.back.search.application.handlers.search_handler import SearchHandler
from src.back.search.infrastructure.searchmodel.tf_idf_search_model import TFIDFSearchModel
from src.back.search.infrastructure.search_model_dependency.tf_idf_search_model_dependency import TfIdfSearchModelDependency

class TfIdfSearchHandler(SearchHandler[TFIDFSearchModel, TfIdfSearchModelDependency]):
    pass