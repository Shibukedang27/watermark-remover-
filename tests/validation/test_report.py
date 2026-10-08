import json
from pathlib import Path

from codecleaner.validation.engine import ValidationEngine
from codecleaner.validation.report import build_report, write_report


def test_report_structure(tmp_path: Path):
    path = tmp_path / "main.py"
    path.write_text("print('hello')\n", encoding="utf-8")

    result = ValidationEngine().validate_project(
        tmp_path,
        [path],
    )

    report = build_report(result)

    assert report["version"] == "1.0"
    assert report["valid"] is True
    assert report["files"] == 1
    assert report["checked_files"] == 1
    assert report["invalid_files"] == 0
    assert report["issues"] == 0


def test_write_report(tmp_path: Path):
    source = tmp_path / "main.py"
    source.write_text("print('hello')\n", encoding="utf-8")

    result = ValidationEngine().validate_project(
        tmp_path,
        [source],
    )

    output = tmp_path / "report.json"
    write_report(output, result)

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["version"] == "1.0"
    assert data["valid"] is True
    assert data["files"] == 1
