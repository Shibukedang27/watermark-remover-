from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re

from codecleaner.detection.models import (
    DetectionFinding,
    FindingAction,
    FindingType,
)
from codecleaner.detection.protection import protect_line


COMMENT_RE = re.compile(r"^\s*(?:#|//|/\*+|<!--|--)")


class ArtifactIntelligence:
    """Detect conservative redundancy patterns that look like generated noise."""

    def scan_file(self, root: Path, path: Path) -> list[DetectionFinding]:
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return []

        relative = str(path.relative_to(root))
        lines = content.splitlines()
        findings: list[DetectionFinding] = []

        seen_comments: dict[str, int] = {}

        for line_number, line in enumerate(lines, start=1):
            if not line.strip() or protect_line(line).protected:
                continue

            stripped = line.strip()

            if COMMENT_RE.match(line):
                normalized = re.sub(r"\s+", " ", stripped)
                if len(normalized) >= 18 and not re.search(
                    r"^#\s*(?:todo|fixme|note|pragma|noqa|type:|region|endregion)\b",
                    normalized,
                    re.IGNORECASE,
                ):
                    previous = seen_comments.get(normalized)
                    seen_comments[normalized] = line_number

                    if previous is not None:
                        raw_id = (
                            f"{relative}:{line_number}:REDUNDANT-COMMENT:{normalized}"
                        )
                        findings.append(
                            DetectionFinding(
                                finding_id=sha256(
                                    raw_id.encode("utf-8")
                                ).hexdigest()[:16],
                                rule_id="REDUNDANT-001",
                                file=relative,
                                line=line_number,
                                finding_type=FindingType.REDUNDANT_CONTENT,
                                action=FindingAction.REMOVE,
                                confidence=0.98,
                                matched_text=line,
                                reason=(
                                    "Duplicate natural-language comment already "
                                    f"appears on line {previous}."
                                ),
                            )
                        )

        for line_number in range(2, len(lines) + 1):
            current = lines[line_number - 1].strip()
            previous = lines[line_number - 2].strip()

            if not current or not previous or current != previous:
                continue

            if COMMENT_RE.match(lines[line_number - 1]):
                continue

            raw_id = f"{relative}:{line_number}:DUPLICATE-LINE:{current}"
            findings.append(
                DetectionFinding(
                    finding_id=sha256(
                        raw_id.encode("utf-8")
                    ).hexdigest()[:16],
                    rule_id="REDUNDANT-002",
                    file=relative,
                    line=line_number,
                    finding_type=FindingType.REDUNDANT_CONTENT,
                    action=FindingAction.REVIEW,
                    confidence=0.91,
                    matched_text=lines[line_number - 1],
                    reason=(
                        "Identical consecutive code line detected. "
                        "It may be accidental duplication, but automatic "
                        "removal could change program behavior."
                    ),
                )
            )

        return findings

    def scan_files(
        self,
        root: Path,
        files: list[Path],
    ) -> list[DetectionFinding]:
        findings: list[DetectionFinding] = []

        for path in files:
            findings.extend(self.scan_file(root, path))

        return findings
