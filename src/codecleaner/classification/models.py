from dataclasses import dataclass
from enum import Enum


class Decision(str, Enum):
    REMOVE = "remove"
    KEEP = "keep"
    REVIEW = "review"


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class ClassifiedFinding:
    finding_id: str
    rule_id: str
    file: str
    line: int
    category: str
    decision: Decision
    severity: Severity
    confidence: float
    matched_text: str
    reason: str

    def to_dict(self) -> dict:
        return {
            "finding_id": self.finding_id,
            "rule_id": self.rule_id,
            "file": self.file,
            "line": self.line,
            "category": self.category,
            "decision": self.decision.value,
            "severity": self.severity.value,
            "confidence": self.confidence,
            "matched_text": self.matched_text,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ClassificationSummary:
    total: int
    remove: int
    keep: int
    review: int
    high: int
    medium: int
    low: int
    info: int

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "remove": self.remove,
            "keep": self.keep,
            "review": self.review,
            "severity": {
                "high": self.high,
                "medium": self.medium,
                "low": self.low,
                "info": self.info,
            },
        }
