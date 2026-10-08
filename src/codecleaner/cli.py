from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from codecleaner.classification.engine import ClassificationEngine
from codecleaner.detection.engine import DetectionEngine
from codecleaner.normalization.engine import NormalizationEngine
from codecleaner.review.engine import ReviewEngine
from codecleaner.review.report import write_diff, write_report as write_review_report
from codecleaner.transformation.engine import TransformationEngine
from codecleaner.validation.engine import ValidationEngine
from codecleaner.validation.report import write_report as write_validation_report


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


def collect_files(root: Path) -> list[Path]:
    files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        relative = path.relative_to(root)

        if any(part in IGNORED_DIRS for part in relative.parts):
            continue

        files.append(path)

    return sorted(files, key=str)


def create_zip(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(
        output,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for path in sorted(source.rglob("*"), key=str):
            if path.is_file():
                archive.write(
                    path,
                    arcname=path.relative_to(source),
                )


def clean_project(
    source: Path,
    output: Path,
    report_dir: Path | None = None,
    zip_path: Path | None = None,
) -> int:
    source = source.expanduser().resolve()
    output = output.expanduser().resolve()

    if not source.exists() or not source.is_dir():
        print(f"error: input directory does not exist: {source}", file=sys.stderr)
        return 2

    if output.exists() and any(output.iterdir()):
        print(f"error: output directory is not empty: {output}", file=sys.stderr)
        return 2

    output.mkdir(parents=True, exist_ok=True)

    source_files = collect_files(source)

    if not source_files:
        print("error: no project files found", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="codecleaner-") as temp:
        workspace = Path(temp)
        original = workspace / "original"
        cleaned = workspace / "cleaned"

        shutil.copytree(source, original)
        shutil.copytree(source, cleaned)

        detection = DetectionEngine()
        findings = detection.scan_files(
            cleaned,
            collect_files(cleaned),
        )

        classified = ClassificationEngine().classify_many(findings)

        transformation = TransformationEngine().transform(
            cleaned,
            workspace / "transformed",
            classified,
        )

        transformed = workspace / "transformed"

        normalization = NormalizationEngine().normalize_project(
            transformed,
            collect_files(transformed),
        )

        validation = ValidationEngine().validate_project(
            transformed,
            collect_files(transformed),
        )

        review = ReviewEngine().build_report(
            original,
            transformed,
            collect_files(transformed),
            findings=len(findings),
        )

        failed_transformations = [
            item for item in transformation
            if item.status.value == "failed"
        ]

        if failed_transformations:
            print("TRANSFORMATION FAILED")
            for item in failed_transformations:
                print(f"  {item.file}: {item.error}")
            return 1

        if not validation.valid:
            print("VALIDATION FAILED")
            print(f"Invalid files: {validation.invalid_files}")
            print(f"Issues: {validation.issues}")
            print("Export aborted.")
            return 1

        shutil.copytree(
            transformed,
            output,
            dirs_exist_ok=True,
        )

        if report_dir is not None:
            report_dir.mkdir(parents=True, exist_ok=True)

            write_review_report(
                report_dir / "review.json",
                review,
            )

            write_diff(
                report_dir / "changes.diff",
                review,
            )

            write_validation_report(
                report_dir / "validation.json",
                validation,
            )

        if zip_path is not None:
            create_zip(
                output,
                zip_path.expanduser().resolve(),
            )

        normalized_files = sum(
            1 for item in normalization
            if item.changed
        )

        print("")
        print("========================================")
        print(" CODECLEANER CLEAN COMPLETE")
        print("========================================")
        print(f"Input:              {source}")
        print(f"Output:             {output}")
        print(f"Files scanned:      {len(source_files)}")
        print(f"AI findings:        {len(findings)}")
        print(f"Files transformed:  {len(transformation)}")
        print(f"Files normalized:   {normalized_files}")
        print(f"Files changed:      {review.changed_files}")
        print(f"Lines removed:      {review.deletions}")
        print("Validation:         PASS")

        if zip_path:
            print(f"ZIP export:         {zip_path}")

        if report_dir:
            print(f"Reports:            {report_dir}")

        print("========================================")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codecleaner",
        description="Safe AI code artifact cleaner.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    clean = subparsers.add_parser(
        "clean",
        help="Clean and validate a project.",
    )

    clean.add_argument(
        "input",
        help="Input project directory.",
    )

    clean.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output directory.",
    )

    clean.add_argument(
        "--report",
        help="Directory for JSON and diff reports.",
    )

    clean.add_argument(
        "--zip",
        help="Optional ZIP export path.",
    )

    clean.set_defaults(handler=clean_project)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "clean":
        return args.handler(
            Path(args.input),
            Path(args.output),
            Path(args.report) if args.report else None,
            Path(args.zip) if args.zip else None,
        )

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
