from dataclasses import dataclass

from src.back.core.domain.value_objects import ValueObject

@dataclass(frozen=True)
class SearchQuery(ValueObject):
    query: str
    top_n: int

    def __post_init__(self):
        if len(self.query) > 1000:
            raise ValueError(f"The query:\n{self.value}\n is too long!")
        if ((self.top_n <= 0) or (self.top_n > 2000)):
            raise ValueError(f"The number of documents to retrieve must be in the range between 1 and 1999")