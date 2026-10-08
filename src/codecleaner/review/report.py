from __future__ import annotations

import json
from pathlib import Path

from codecleaner.review.models import ReviewReport


def build_report(report: ReviewReport) -> dict:
    return {
        "version": "1.0",
        "findings": report.findings,
        "files": len(report.files),
        "changed_files": report.changed_files,
        "additions": report.additions,
        "deletions": report.deletions,
        "changes": report.changes,
        "has_changes": report.has_changes,
        "files_detail": [
            {
                "file": item.file,
                "status": item.status,
                "additions": item.additions,
                "deletions": item.deletions,
                "changes": item.changes,
                "diff": item.diff,
            }
            for item in report.files
        ],
    }


def write_report(path: Path, report: ReviewReport) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_report(report), indent=2),
        encoding="utf-8",
    )


def write_diff(path: Path, report: ReviewReport) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    content = "\n".join(
        item.diff
        for item in report.files
        if item.diff
    )

    path.write_text(content, encoding="utf-8")
