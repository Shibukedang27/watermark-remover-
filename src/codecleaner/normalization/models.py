from dataclasses import dataclass
from enum import Enum


class NormalizationType(str, Enum):
    TRAILING_WHITESPACE = "trailing_whitespace"
    MULTIPLE_BLANK_LINES = "multiple_blank_lines"
    MISSING_FINAL_NEWLINE = "missing_final_newline"


@dataclass(frozen=True)
class NormalizationChange:
    file: str
    change_type: NormalizationType
    line: int | None
    description: str

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "change_type": self.change_type.value,
            "line": self.line,
            "description": self.description,
        }


@dataclass(frozen=True)
class NormalizationResult:
    file: str
    changed: bool
    changes: tuple[NormalizationChange, ...]

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "changed": self.changed,
            "changes": [
                change.to_dict()
                for change in self.changes
            ],
        }
