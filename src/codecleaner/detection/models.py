from dataclasses import dataclass
from enum import Enum


class FindingType(str, Enum):
    AI_ATTRIBUTION = "ai_attribution"
    GENERATED_BANNER = "generated_banner"
    TOOL_NOTICE = "tool_notice"
    AI_ASSISTANT_MARKER = "ai_assistant_marker"


class FindingAction(str, Enum):
    KEEP = "keep"
    REMOVE = "remove"
    REVIEW = "review"


@dataclass(frozen=True)
class DetectionFinding:
    finding_id: str
    rule_id: str
    file: str
    line: int
    finding_type: FindingType
    action: FindingAction
    confidence: float
    matched_text: str
    reason: str

    def to_dict(self) -> dict:
        return {
            "finding_id": self.finding_id,
            "rule_id": self.rule_id,
            "file": self.file,
            "line": self.line,
            "finding_type": self.finding_type.value,
            "action": self.action.value,
            "confidence": self.confidence,
            "matched_text": self.matched_text,
            "reason": self.reason,
        }
