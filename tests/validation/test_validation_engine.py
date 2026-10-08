from pathlib import Path

from codecleaner.validation.engine import ValidationEngine
from codecleaner.validation.models import (
    ValidationStatus,
    ValidationType,
)


def test_valid_python(tmp_path: Path):
    path = tmp_path / "main.py"
    path.write_text("print('hello')\n", encoding="utf-8")

    result = ValidationEngine().validate_file(tmp_path, path)

    assert result.status == ValidationStatus.VALID
    assert result.validation_type == ValidationType.PYTHON_SYNTAX
    assert result.issues == ()


def test_invalid_python(tmp_path: Path):
    path = tmp_path / "main.py"
    path.write_text("def broken(:\n", encoding="utf-8")

    result = ValidationEngine().validate_file(tmp_path, path)

    assert result.status == ValidationStatus.INVALID
    assert result.validation_type == ValidationType.PYTHON_SYNTAX
    assert len(result.issues) == 1
    assert result.issues[0].line == 1


def test_valid_javascript(tmp_path: Path):
    path = tmp_path / "main.js"
    path.write_text(
        "function hello() { return 'world'; }\n",
        encoding="utf-8",
    )

    result = ValidationEngine().validate_file(tmp_path, path)

    assert result.status == ValidationStatus.VALID


def test_invalid_javascript(tmp_path: Path):
    path = tmp_path / "main.js"
    path.write_text(
        "function hello( {\n",
        encoding="utf-8",
    )

    result = ValidationEngine().validate_file(tmp_path, path)

    assert result.status == ValidationStatus.INVALID
    assert len(result.issues) >= 1


def test_unsupported_file_is_skipped(tmp_path: Path):
    path = tmp_path / "image.bin"
    path.write_bytes(b"\x00\x01\x02")

    result = ValidationEngine().validate_file(tmp_path, path)

    assert result.status == ValidationStatus.SKIPPED
    assert result.validation_type == ValidationType.UNSUPPORTED


def test_project_validation(tmp_path: Path):
    python_file = tmp_path / "main.py"
    js_file = tmp_path / "app.js"

    python_file.write_text("print('ok')\n", encoding="utf-8")
    js_file.write_text("const x = 1;\n", encoding="utf-8")

    result = ValidationEngine().validate_project(
        tmp_path,
        [python_file, js_file],
    )

    assert result.valid
    assert result.checked_files == 2
    assert result.invalid_files == 0
    assert result.issues == 0


def test_project_validation_detects_failure(tmp_path: Path):
    good = tmp_path / "good.py"
    bad = tmp_path / "bad.py"

    good.write_text("x = 1\n", encoding="utf-8")
    bad.write_text("def broken(:\n", encoding="utf-8")

    result = ValidationEngine().validate_project(
        tmp_path,
        [good, bad],
    )

    assert not result.valid
    assert result.checked_files == 2
    assert result.invalid_files == 1
    assert result.issues == 1
