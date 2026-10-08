from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ValidationStatus(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    SKIPPED = "skipped"


class ValidationType(str, Enum):
    PYTHON_SYNTAX = "python_syntax"
    TREE_SITTER = "tree_sitter"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class ValidationIssue:
    file: str
    validation_type: ValidationType
    line: int | None
    column: int | None
    message: str


@dataclass(frozen=True)
class FileValidation:
    file: str
    status: ValidationStatus
    validation_type: ValidationType
    issues: tuple[ValidationIssue, ...] = ()


@dataclass(frozen=True)
class ValidationResult:
    files: tuple[FileValidation, ...]

    @property
    def valid(self) -> bool:
        return all(
            item.status != ValidationStatus.INVALID
            for item in self.files
        )

    @property
    def checked_files(self) -> int:
        return sum(
            item.status != ValidationStatus.SKIPPED
            for item in self.files
        )

    @property
    def invalid_files(self) -> int:
        return sum(
            item.status == ValidationStatus.INVALID
            for item in self.files
        )

    @property
    def skipped_files(self) -> int:
        return sum(
            item.status == ValidationStatus.SKIPPED
            for item in self.files
        )

    @property
    def issues(self) -> int:
        return sum(len(item.issues) for item in self.files)
