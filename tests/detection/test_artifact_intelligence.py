from pathlib import Path

from codecleaner.detection.engine import DetectionEngine
from codecleaner.detection.models import FindingAction, FindingType
from codecleaner.normalization.engine import NormalizationEngine
from codecleaner.normalization.models import NormalizationType


def test_repeated_comment_is_removable(tmp_path):
    source = tmp_path / "main.py"
    source.write_text(
        "# This is generated explanatory noise that repeats\n"
        "print('hello')\n"
        "# This is generated explanatory noise that repeats\n",
        encoding="utf-8",
    )

    findings = DetectionEngine().scan_file(tmp_path, source)

    redundant = [
        item for item in findings
        if item.rule_id == "REDUNDANT-001"
    ]

    assert len(redundant) == 1
    assert redundant[0].finding_type == FindingType.REDUNDANT_CONTENT
    assert redundant[0].action == FindingAction.REMOVE
    assert redundant[0].line == 3


def test_repeated_code_line_requires_review(tmp_path):
    source = tmp_path / "main.py"
    source.write_text(
        "x = 1\n"
        "x = 1\n",
        encoding="utf-8",
    )

    findings = DetectionEngine().scan_file(tmp_path, source)

    redundant = [
        item for item in findings
        if item.rule_id == "REDUNDANT-002"
    ]

    assert len(redundant) == 1
    assert redundant[0].action == FindingAction.REVIEW
    assert redundant[0].line == 2


def test_normalization_removes_edge_spacing(tmp_path):
    source = tmp_path / "main.py"
    source.write_text(
        "\n"
        "\n"
        "print('hello')\n"
        "\n"
        "\n",
        encoding="utf-8",
    )

    result = NormalizationEngine().normalize_file(tmp_path, source)

    assert result.changed
    assert source.read_text(encoding="utf-8") == "print('hello')\n"
    types = {change.change_type for change in result.changes}
    assert NormalizationType.LEADING_BLANK_LINES in types
    assert NormalizationType.TRAILING_BLANK_LINES in types
