from hashlib import sha256
from pathlib import Path
import shutil

from codecleaner.classification.models import ClassifiedFinding, Decision
from .models import FileTransformation, TransformStatus


class TransformationEngine:
    """
    Applies only explicitly classified REMOVE findings.

    The source project is never modified directly.
    """

    def transform(
        self,
        source_root: Path,
        output_root: Path,
        findings: list[ClassifiedFinding],
    ) -> list[FileTransformation]:

        if output_root.exists():
            shutil.rmtree(output_root)

        shutil.copytree(source_root, output_root)

        removable = {}

        for finding in findings:
            if finding.decision != Decision.REMOVE:
                continue

            path = output_root / finding.file
            removable.setdefault(path, set()).add(finding.line)

        results = []

        for path, lines in removable.items():
            relative = str(path.relative_to(output_root))

            try:
                original_bytes = path.read_bytes()
                original_hash = sha256(original_bytes).hexdigest()

                original_lines = original_bytes.decode(
                    "utf-8"
                ).splitlines(keepends=True)

                cleaned_lines = [
                    line
                    for number, line in enumerate(
                        original_lines,
                        start=1,
                    )
                    if number not in lines
                ]

                output_text = "".join(cleaned_lines)
                output_bytes = output_text.encode("utf-8")

                if output_bytes == original_bytes:
                    results.append(
                        FileTransformation(
                            file=relative,
                            status=TransformStatus.UNCHANGED,
                            removed_lines=0,
                            original_sha256=original_hash,
                            output_sha256=original_hash,
                        )
                    )
                    continue

                path.write_bytes(output_bytes)

                output_hash = sha256(output_bytes).hexdigest()

                results.append(
                    FileTransformation(
                        file=relative,
                        status=TransformStatus.CHANGED,
                        removed_lines=len(lines),
                        original_sha256=original_hash,
                        output_sha256=output_hash,
                    )
                )

            except Exception as exc:
                results.append(
                    FileTransformation(
                        file=relative,
                        status=TransformStatus.FAILED,
                        removed_lines=0,
                        original_sha256="",
                        output_sha256="",
                        error=str(exc),
                    )
                )

        return results
