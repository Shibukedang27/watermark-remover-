import json
from pathlib import Path

from codecleaner.review.engine import ReviewEngine
from codecleaner.review.report import build_report, write_diff, write_report


def test_json_report(tmp_path: Path):
    original = tmp_path / "original"
    cleaned = tmp_path / "cleaned"

    original.mkdir()
    cleaned.mkdir()

    (original / "main.py").write_text(
        "# AI generated\nprint('hello')\n",
        encoding="utf-8",
    )
    (cleaned / "main.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    report = ReviewEngine().build_report(
        original,
        cleaned,
        [],
        findings=1,
    )

    output = tmp_path / "review.json"
    write_report(output, report)

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["version"] == "1.0"
    assert data["findings"] == 1
    assert data["changed_files"] == 1
    assert data["deletions"] == 1


def test_diff_report(tmp_path: Path):
    original = tmp_path / "original"
    cleaned = tmp_path / "cleaned"

    original.mkdir()
    cleaned.mkdir()

    (original / "main.py").write_text(
        "# AI generated\nprint('hello')\n",
        encoding="utf-8",
    )
    (cleaned / "main.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    report = ReviewEngine().build_report(
        original,
        cleaned,
        [],
    )

    output = tmp_path / "review.diff"
    write_diff(output, report)

    text = output.read_text(encoding="utf-8")

    assert "--- main.py" in text
    assert "+++ main.py" in text
    assert "-# AI generated" in text


def test_report_builder_is_serializable(tmp_path: Path):
    original = tmp_path / "original"
    cleaned = tmp_path / "cleaned"

    original.mkdir()
    cleaned.mkdir()

    (original / "main.py").write_text(
        "print('a')\n",
        encoding="utf-8",
    )
    (cleaned / "main.py").write_text(
        "print('b')\n",
        encoding="utf-8",
    )

    report = ReviewEngine().build_report(
        original,
        cleaned,
        [],
    )

    data = build_report(report)

    assert isinstance(data, dict)
    assert data["files"] == 1
    assert isinstance(data["files_detail"], list)
