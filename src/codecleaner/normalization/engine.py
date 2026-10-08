from __future__ import annotations

from pathlib import Path

from codecleaner.normalization.models import (
    NormalizationChange,
    NormalizationResult,
    NormalizationType,
)


class NormalizationEngine:
    """Apply conservative, opt-in source-code normalization."""

    def normalize_file(
        self,
        root: Path,
        path: Path,
        dry_run: bool = False,
    ) -> NormalizationResult:
        root = Path(root)
        path = Path(path)

        relative = path.relative_to(root)
        original = path.read_text(encoding="utf-8")

        changes: list[NormalizationChange] = []
        normalized = original

        # 1. Remove trailing whitespace while preserving line structure.
        lines = normalized.splitlines()

        stripped_lines = [line.rstrip() for line in lines]

        if stripped_lines != lines:
            changes.append(
                NormalizationChange(
                    file=str(relative),
                    change_type=NormalizationType.TRAILING_WHITESPACE,
                    line=None,
                    description="Removed trailing whitespace.",
                )
            )

        # 2. Collapse consecutive blank lines.
        collapsed: list[str] = []
        previous_blank = False

        for line in stripped_lines:
            blank = line.strip() == ""

            if blank and previous_blank:
                continue

            collapsed.append(line)
            previous_blank = blank

        if collapsed != stripped_lines:
            changes.append(
                NormalizationChange(
                    file=str(relative),
                    change_type=NormalizationType.MULTIPLE_BLANK_LINES,
                    line=None,
                    description="Collapsed consecutive blank lines.",
                )
            )

        # 3. Reconstruct while preserving whether the original had
        #    a final newline.
        normalized = "\n".join(collapsed)

        if original.endswith("\n"):
            normalized += "\n"

        # 4. Add a final newline only if the ORIGINAL file lacked one.
        if original and not original.endswith("\n"):
            normalized += "\n"
            changes.append(
                NormalizationChange(
                    file=str(relative),
                    change_type=NormalizationType.MISSING_FINAL_NEWLINE,
                    line=None,
                    description="Added final newline.",
                )
            )

        changed = normalized != original

        if changed and not dry_run:
            path.write_text(normalized, encoding="utf-8")

        return NormalizationResult(
            file=str(relative),
            changed=changed,
            changes=tuple(changes),
        )

    def normalize_project(
        self,
        root: Path,
        files: list[Path],
        dry_run: bool = False,
    ) -> tuple[NormalizationResult, ...]:
        return tuple(
            self.normalize_file(root, path, dry_run=dry_run)
            for path in files
        )
