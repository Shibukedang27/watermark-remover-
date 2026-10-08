from pathlib import Path
import difflib


def generate_file_diff(
    original: Path,
    cleaned: Path,
) -> str:
    original_lines = original.read_text(
        encoding="utf-8"
    ).splitlines(keepends=True)

    cleaned_lines = cleaned.read_text(
        encoding="utf-8"
    ).splitlines(keepends=True)

    return "".join(
        difflib.unified_diff(
            original_lines,
            cleaned_lines,
            fromfile=str(original),
            tofile=str(cleaned),
        )
    )


def generate_project_diff(
    original_root: Path,
    cleaned_root: Path,
    files: list[str],
) -> str:
    chunks = []

    for relative in files:
        original = original_root / relative
        cleaned = cleaned_root / relative

        if original.exists() and cleaned.exists():
            diff = generate_file_diff(original, cleaned)

            if diff:
                chunks.append(diff)

    return "\n".join(chunks)
