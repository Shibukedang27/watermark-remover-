from collections import Counter

from codecleaner.detection.models import DetectionFinding
from .models import (
    ClassifiedFinding,
    ClassificationSummary,
    Decision,
    Severity,
)


class ClassificationEngine:

    def classify(self, finding: DetectionFinding) -> ClassifiedFinding:
        confidence = finding.confidence

        if finding.action.value == "remove" and confidence >= 0.97:
            decision = Decision.REMOVE
            severity = Severity.LOW

        elif finding.action.value == "remove" and confidence >= 0.90:
            decision = Decision.REVIEW
            severity = Severity.MEDIUM

        elif finding.action.value == "review":
            decision = Decision.REVIEW
            severity = Severity.MEDIUM

        else:
            decision = Decision.KEEP
            severity = Severity.INFO

        return ClassifiedFinding(
            finding_id=finding.finding_id,
            rule_id=finding.rule_id,
            file=finding.file,
            line=finding.line,
            category=finding.finding_type.value,
            decision=decision,
            severity=severity,
            confidence=confidence,
            matched_text=finding.matched_text,
            reason=finding.reason,
        )

    def classify_many(
        self,
        findings: list[DetectionFinding],
    ) -> list[ClassifiedFinding]:
        return [self.classify(finding) for finding in findings]

    def summarize(
        self,
        findings: list[ClassifiedFinding],
    ) -> ClassificationSummary:
        decisions = Counter(item.decision for item in findings)
        severity = Counter(item.severity for item in findings)

        return ClassificationSummary(
            total=len(findings),
            remove=decisions[Decision.REMOVE],
            keep=decisions[Decision.KEEP],
            review=decisions[Decision.REVIEW],
            high=severity[Severity.HIGH],
            medium=severity[Severity.MEDIUM],
            low=severity[Severity.LOW],
            info=severity[Severity.INFO],
        )
