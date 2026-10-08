from pathlib import Path

from codecleaner.parsers.engine import parse_file

FIXTURES = Path(__file__).parent / "fixtures"


def test_python_parser():
    result = parse_file(FIXTURES / "sample.py")

    assert result.language == "python"
    assert result.success
    assert result.root_type == "module"


def test_javascript_parser():
    result = parse_file(FIXTURES / "sample.js")

    assert result.language == "javascript"
    assert result.success
    assert result.root_type == "program"


def test_unknown_file():
    result = parse_file(FIXTURES / "sample.unknown")

    assert not result.success
    assert result.language == "unknown"
