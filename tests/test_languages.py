from pathlib import Path

from codecleaner.core.languages import detect_language


def test_python_detection():
    assert detect_language(Path("main.py")) == "python"


def test_typescript_detection():
    assert detect_language(Path("app.tsx")) == "typescript"


def test_unknown_detection():
    assert detect_language(Path("file.xyz")) is None
