from __future__ import annotations

import ast
from pathlib import Path

from codecleaner.core.languages import detect_language
from codecleaner.parsers.engine import parse_file
from codecleaner.validation.models import (
    FileValidation,
    ValidationIssue,
    ValidationResult,
    ValidationStatus,
    ValidationType,
)


class ValidationEngine:
    """
    Safely validate source files without executing project code.

    Python files use the standard-library AST compiler.
    Other supported parser languages use the existing Tree-sitter
    parser infrastructure.
    """

    def validate_file(
        self,
        root: Path,
        path: Path,
    ) -> FileValidation:
        root = Path(root)
        path = Path(path)
        relative = str(path.relative_to(root))

        language = detect_language(path)

        if language is None:
            return FileValidation(
                file=relative,
                status=ValidationStatus.SKIPPED,
                validation_type=ValidationType.UNSUPPORTED,
            )

        if language == "python":
            return self._validate_python(root, path)

        return self._validate_tree_sitter(root, path)

    def _validate_python(
        self,
        root: Path,
        path: Path,
    ) -> FileValidation:
        relative = str(path.relative_to(root))

        try:
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=relative)
        except SyntaxError as exc:
            issue = ValidationIssue(
                file=relative,
                validation_type=ValidationType.PYTHON_SYNTAX,
                line=exc.lineno,
                column=exc.offset,
                message=exc.msg,
            )
            return FileValidation(
                file=relative,
                status=ValidationStatus.INVALID,
                validation_type=ValidationType.PYTHON_SYNTAX,
                issues=(issue,),
            )
        except (UnicodeDecodeError, OSError) as exc:
            issue = ValidationIssue(
                file=relative,
                validation_type=ValidationType.PYTHON_SYNTAX,
                line=None,
                column=None,
                message=str(exc),
            )
            return FileValidation(
                file=relative,
                status=ValidationStatus.INVALID,
                validation_type=ValidationType.PYTHON_SYNTAX,
                issues=(issue,),
            )

        return FileValidation(
            file=relative,
            status=ValidationStatus.VALID,
            validation_type=ValidationType.PYTHON_SYNTAX,
        )

    def _validate_tree_sitter(
        self,
        root: Path,
        path: Path,
    ) -> FileValidation:
        relative = str(path.relative_to(root))

        try:
            result = parse_file(path)
        except Exception as exc:
            issue = ValidationIssue(
                file=relative,
                validation_type=ValidationType.TREE_SITTER,
                line=None,
                column=None,
                message=str(exc),
            )
            return FileValidation(
                file=relative,
                status=ValidationStatus.INVALID,
                validation_type=ValidationType.TREE_SITTER,
                issues=(issue,),
            )

        if getattr(result, "success", False):
            return FileValidation(
                file=relative,
                status=ValidationStatus.VALID,
                validation_type=ValidationType.TREE_SITTER,
            )

        errors = getattr(result, "errors", None) or []

        if not errors:
            errors = ["Parser reported an invalid syntax tree."]

        issues = tuple(
            ValidationIssue(
                file=relative,
                validation_type=ValidationType.TREE_SITTER,
                line=None,
                column=None,
                message=str(error),
            )
            for error in errors
        )

        return FileValidation(
            file=relative,
            status=ValidationStatus.INVALID,
            validation_type=ValidationType.TREE_SITTER,
            issues=issues,
        )

    def validate_project(
        self,
        root: Path,
        files: list[Path] | tuple[Path, ...],
    ) -> ValidationResult:
        results = tuple(
            self.validate_file(root, Path(path))
            for path in sorted(files, key=lambda item: str(item))
        )
        return ValidationResult(files=results)
