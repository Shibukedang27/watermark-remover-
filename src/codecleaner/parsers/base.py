from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ParseResult:
    language: str
    success: bool
    root_type: str | None = None
    error: str | None = None


class Parser(ABC):
    language: str

    @abstractmethod
    def parse(self, source: bytes) -> ParseResult:
        raise NotImplementedError
