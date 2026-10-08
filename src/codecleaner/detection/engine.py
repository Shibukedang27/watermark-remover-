from pathlib import Path
from hashlib import sha256

from .models import DetectionFinding
from .rules import RULES
from .protection import protect_line


class DetectionEngine:
    def __init__(self, rules=RULES):
        self.rules = tuple(rules)

    def scan_file(self, root: Path, path: Path) -> list[DetectionFinding]:
        findings: list[DetectionFinding] = []

        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return findings

        relative = str(path.relative_to(root))

        for line_number, line in enumerate(content.splitlines(), start=1):
            protection = protect_line(line)

            if protection.protected:
                continue

            for rule in self.rules:
                if not rule.pattern.match(line):
                    continue

                raw_id = f"{relative}:{line_number}:{rule.rule_id}:{line}"
                finding_id = sha256(raw_id.encode("utf-8")).hexdigest()[:16]

                findings.append(
                    DetectionFinding(
                        finding_id=finding_id,
                        rule_id=rule.rule_id,
                        file=relative,
                        line=line_number,
                        finding_type=rule.finding_type,
                        action=rule.action,
                        confidence=rule.confidence,
                        matched_text=line,
                        reason=rule.reason,
                    )
                )

        return findings

    def scan_files(self, root: Path, files: list[Path]) -> list[DetectionFinding]:
        findings = []

        for path in files:
            findings.extend(self.scan_file(root, path))

        return findings
