import json
from pathlib import Path

from .models import ClassifiedFinding, ClassificationSummary


def build_report(
    findings: list[ClassifiedFinding],
    summary: ClassificationSummary,
) -> dict:
    return {
        "version": "1.0",
        "findings": [finding.to_dict() for finding in findings],
        "summary": summary.to_dict(),
    }


def write_report(
    path: Path,
    findings: list[ClassifiedFinding],
    summary: ClassificationSummary,
) -> None:
    report = build_report(findings, summary)

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
