from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewFile:
    file: str
    status: str
    additions: int
    deletions: int
    changes: int
    diff: str


@dataclass(frozen=True)
class ReviewReport:
    files: tuple[ReviewFile, ...]
    findings: int
    changed_files: int
    additions: int
    deletions: int
    changes: int

    @property
    def has_changes(self) -> bool:
        return self.changed_files > 0
