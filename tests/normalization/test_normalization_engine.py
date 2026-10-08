from pathlib import Path

from codecleaner.normalization.engine import NormalizationEngine
from codecleaner.normalization.models import NormalizationType


def test_trailing_whitespace(tmp_path: Path):
    path = tmp_path / "main.py"

    path.write_text(
        "print('hello')   \n",
        encoding="utf-8",
    )

    result = NormalizationEngine().normalize_file(
        tmp_path,
        path,
    )

    assert result.changed
    assert any(
        change.change_type
        == NormalizationType.TRAILING_WHITESPACE
        for change in result.changes
    )

    assert path.read_text(
        encoding="utf-8"
    ) == "print('hello')\n"


def test_multiple_blank_lines(tmp_path: Path):
    path = tmp_path / "main.py"

    path.write_text(
        "print('a')\n"
        "\n"
        "\n"
        "\n"
        "print('b')\n",
        encoding="utf-8",
    )

    result = NormalizationEngine().normalize_file(
        tmp_path,
        path,
    )

    assert result.changed

    assert path.read_text(
        encoding="utf-8"
    ) == (
        "print('a')\n"
        "\n"
        "print('b')\n"
    )


def test_adds_final_newline(tmp_path: Path):
    path = tmp_path / "main.py"

    path.write_text(
        "print('hello')",
        encoding="utf-8",
    )

    result = NormalizationEngine().normalize_file(
        tmp_path,
        path,
    )

    assert result.changed

    assert path.read_text(
        encoding="utf-8"
    ).endswith("\n")


def test_dry_run_does_not_modify(tmp_path: Path):
    path = tmp_path / "main.py"

    original = "print('hello')   "
    path.write_text(
        original,
        encoding="utf-8",
    )

    result = NormalizationEngine().normalize_file(
        tmp_path,
        path,
        dry_run=True,
    )

    assert result.changed
    assert path.read_text(
        encoding="utf-8"
    ) == original


def test_clean_file_is_unchanged(tmp_path: Path):
    path = tmp_path / "main.py"

    original = "print('hello')\n"

    path.write_text(
        original,
        encoding="utf-8",
    )

    result = NormalizationEngine().normalize_file(
        tmp_path,
        path,
    )

    assert not result.changed
    assert result.changes == ()
