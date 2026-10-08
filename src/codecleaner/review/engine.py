from __future__ import annotations

import difflib
from pathlib import Path

from codecleaner.review.models import ReviewFile, ReviewReport


class ReviewEngine:
    """Build safe human-readable review data from original/cleaned trees."""

    def compare_file(
        self,
        root_original: Path,
        root_cleaned: Path,
        relative: Path,
    ) -> ReviewFile:
        original_path = Path(root_original) / relative
        cleaned_path = Path(root_cleaned) / relative

        original = (
            original_path.read_text(encoding="utf-8")
            if original_path.exists()
            else ""
        )
        cleaned = (
            cleaned_path.read_text(encoding="utf-8")
            if cleaned_path.exists()
            else ""
        )

        if original == cleaned:
            return ReviewFile(
                file=str(relative),
                status="unchanged",
                additions=0,
                deletions=0,
                changes=0,
                diff="",
            )

        diff_lines = list(
            difflib.unified_diff(
                original.splitlines(keepends=True),
                cleaned.splitlines(keepends=True),
                fromfile=str(relative),
                tofile=str(relative),
                lineterm="",
            )
        )

        additions = sum(
            1
            for line in diff_lines
            if line.startswith("+") and not line.startswith("+++")
        )
        deletions = sum(
            1
            for line in diff_lines
            if line.startswith("-") and not line.startswith("---")
        )

        return ReviewFile(
            file=str(relative),
            status="changed",
            additions=additions,
            deletions=deletions,
            changes=additions + deletions,
            diff="".join(diff_lines),
        )

    def build_report(
        self,
        original_root: Path,
        cleaned_root: Path,
        files: list[Path] | tuple[Path, ...],
        findings: int = 0,
    ) -> ReviewReport:
        all_paths = set()

        for root in (Path(original_root), Path(cleaned_root)):
            for path in root.rglob("*"):
                if path.is_file():
                    all_paths.add(path.relative_to(root))

        all_paths.update(Path(item) for item in files)

        results = tuple(
            self.compare_file(
                Path(original_root),
                Path(cleaned_root),
                relative,
            )
            for relative in sorted(all_paths, key=str)
        )

        changed = tuple(
            item for item in results
            if item.status == "changed"
        )

        return ReviewReport(
            files=results,
            findings=findings,
            changed_files=len(changed),
            additions=sum(item.additions for item in changed),
            deletions=sum(item.deletions for item in changed),
            changes=sum(item.changes for item in changed),
        )
