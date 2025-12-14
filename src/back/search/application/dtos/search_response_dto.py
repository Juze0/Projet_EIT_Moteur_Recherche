from dataclasses import dataclass

@dataclass(frozen=True)
class SearchResultDTO:
    document_name: str
    #document_first_line: str TODO à valoriser
    score: float


@dataclass(frozen=True)
class SearchResponseDTO:
    query: str
    results: list[SearchResultDTO]

    def __str__(self) -> str:
        lines = [f"Query: '{self.query}'", "Results:"]
        for idx, result in enumerate(self.results, start=1):
            lines.append(
                f"  {idx}. {result.document_name} (score={result.score:.4f})"
            )
        return "\n".join(lines)