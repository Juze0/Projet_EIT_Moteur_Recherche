from dataclasses import dataclass

from src.back.core.domain.value_objects import ValueObject

@dataclass(frozen=True)
class SearchModelName(ValueObject):
    value: str

    VALID = {"embedding", "tfidf"}

    def __post_init__(self):
        if self.value not in self.VALID:
            raise ValueError(f"Invalid model: {self.value}")
