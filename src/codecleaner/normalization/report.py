import json
from pathlib import Path

from .models import NormalizationResult


def build_report(
    results: list[NormalizationResult],
) -> dict:

    changes = [
        change.to_dict()
        for result in results
        for change in result.changes
    ]

    return {
        "version": "1.0",
        "files": len(results),
        "changed_files": sum(
            result.changed
            for result in results
        ),
        "changes": len(changes),
        "details": [
            result.to_dict()
            for result in results
        ],
    }


def write_report(
    path: Path,
    results: list[NormalizationResult],
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            build_report(results),
            indent=2,
        ),
        encoding="utf-8",
    )
