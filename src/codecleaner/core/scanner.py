from pathlib import Path

from .languages import detect_language, SUPPORTED_TEXT
from .models import Finding, ScanResult, Action
from .rules import classify_line, is_legal_or_copyright_notice


IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".next",
    "dist",
    "build",
    "target",
}


def iter_source_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in IGNORED_DIRS for part in path.parts):
            continue

        if path.suffix.lower() not in SUPPORTED_TEXT:
            continue

        yield path


def scan_project(root: Path) -> ScanResult:
    findings = []
    files_scanned = 0

    for path in iter_source_files(root):
        files_scanned += 1

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for number, line in enumerate(text.splitlines(), start=1):
            if is_legal_or_copyright_notice(line):
                continue

            rule = classify_line(line)

            if rule:
                findings.append(
                    Finding(
                        file=str(path.relative_to(root)),
                        line=number,
                        category=rule.category,
                        action=Action.REMOVE,
                        confidence=rule.confidence,
                        text=line,
                        reason=rule.reason,
                    )
                )

    return ScanResult(
        root=str(root),
        files_scanned=files_scanned,
        findings=findings,
    )
