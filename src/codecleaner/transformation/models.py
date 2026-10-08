from dataclasses import dataclass
from enum import Enum


class TransformStatus(str, Enum):
    CHANGED = "changed"
    UNCHANGED = "unchanged"
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass(frozen=True)
class FileTransformation:
    file: str
    status: TransformStatus
    removed_lines: int
    original_sha256: str
    output_sha256: str
    error: str | None = None

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "status": self.status.value,
            "removed_lines": self.removed_lines,
            "original_sha256": self.original_sha256,
            "output_sha256": self.output_sha256,
            "error": self.error,
        }
