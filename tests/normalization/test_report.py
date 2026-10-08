import json
from pathlib import Path

from codecleaner.normalization.engine import NormalizationEngine
from codecleaner.normalization.report import write_report


def test_normalization_report(tmp_path: Path):
    path = tmp_path / "main.py"

    path.write_text(
        "print('hello')   ",
        encoding="utf-8",
    )

    engine = NormalizationEngine()

    result = engine.normalize_file(
        tmp_path,
        path,
        dry_run=True,
    )

    output = tmp_path / "report.json"

    write_report(
        output,
        [result],
    )

    data = json.loads(
        output.read_text(
            encoding="utf-8"
        )
    )

    assert data["version"] == "1.0"
    assert data["files"] == 1
    assert data["changed_files"] == 1
    assert data["changes"] >= 1
