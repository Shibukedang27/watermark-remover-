from tree_sitter import Language, Parser as TSParser

from .base import ParseResult, Parser


class TreeSitterParser(Parser):
    def __init__(self, language: str, grammar):
        self.language = language
        self._parser = TSParser(Language(grammar))

    def parse(self, source: bytes) -> ParseResult:
        try:
            tree = self._parser.parse(source)

            if tree.root_node is None:
                return ParseResult(
                    language=self.language,
                    success=False,
                    error="Parser returned no root node.",
                )

            has_errors = tree.root_node.has_error

            return ParseResult(
                language=self.language,
                success=not has_errors,
                root_type=tree.root_node.type,
                error="Syntax errors detected." if has_errors else None,
            )

        except Exception as exc:
            return ParseResult(
                language=self.language,
                success=False,
                error=str(exc),
            )
