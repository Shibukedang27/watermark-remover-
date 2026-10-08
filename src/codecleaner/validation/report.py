from __future__ import annotations

import json
from pathlib import Path

from codecleaner.validation.models import ValidationResult


def build_report(result: ValidationResult) -> dict:
    return {
        "version": "1.0",
        "valid": result.valid,
        "files": len(result.files),
        "checked_files": result.checked_files,
        "invalid_files": result.invalid_files,
        "skipped_files": result.skipped_files,
        "issues": result.issues,
        "results": [
            {
                "file": item.file,
                "status": item.status.value,
                "validation_type": item.validation_type.value,
                "issues": [
                    {
                        "file": issue.file,
                        "validation_type": issue.validation_type.value,
                        "line": issue.line,
                        "column": issue.column,
                        "message": issue.message,
                    }
                    for issue in item.issues
                ],
            }
            for item in result.files
        ],
    }


def write_report(path: Path, result: ValidationResult) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_report(result), indent=2),
        encoding="utf-8",
    )
