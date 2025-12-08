from dataclasses import dataclass

from src.back.core.domain.value_objects import ValueObject

@dataclass(frozen=True)
class PreprocessorName(ValueObject):
    value: str

    VALID = {"spacy", "nltk"}

    def __post_init__(self):
        if self.value not in self.VALID:
            raise ValueError(f"Invalid preprocessor: {self.value}")
