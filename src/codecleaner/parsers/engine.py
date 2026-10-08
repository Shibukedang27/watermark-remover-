from pathlib import Path

from ..core.languages import detect_language
from .base import ParseResult
from .registry import parser_for_language


def parse_file(path: Path) -> ParseResult:
    language = detect_language(path)

    if language is None:
        return ParseResult(
            language="unknown",
            success=False,
            error="Unsupported file type.",
        )

    parser = parser_for_language(language)

    if parser is None:
        return ParseResult(
            language=language,
            success=False,
            error="Parser not implemented yet.",
        )

    try:
        source = path.read_bytes()
    except OSError as exc:
        return ParseResult(
            language=language,
            success=False,
            error=str(exc),
        )

    return parser.parse(source)
