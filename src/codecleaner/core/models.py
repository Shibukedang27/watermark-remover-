from dataclasses import dataclass, asdict
from enum import Enum


class Action(str, Enum):
    KEEP = "keep"
    REMOVE = "remove"
    REVIEW = "review"


@dataclass
class Finding:
    file: str
    line: int
    category: str
    action: Action
    confidence: float
    text: str
    reason: str

    def to_dict(self):
        data = asdict(self)
        data["action"] = self.action.value
        return data


@dataclass
class ScanResult:
    root: str
    files_scanned: int
    findings: list[Finding]

    def to_dict(self):
        return {
            "root": self.root,
            "files_scanned": self.files_scanned,
            "findings": [f.to_dict() for f in self.findings],
        }
