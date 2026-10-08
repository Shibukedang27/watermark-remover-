import tree_sitter_python
import tree_sitter_javascript
import tree_sitter_typescript
import tree_sitter_html
import tree_sitter_css
import tree_sitter_json
import tree_sitter_yaml

from .treesitter import TreeSitterParser


PARSERS = {
    "python": TreeSitterParser(
        "python",
        tree_sitter_python.language(),
    ),
    "javascript": TreeSitterParser(
        "javascript",
        tree_sitter_javascript.language(),
    ),
    "typescript": TreeSitterParser(
        "typescript",
        tree_sitter_typescript.language_typescript(),
    ),
    "html": TreeSitterParser(
        "html",
        tree_sitter_html.language(),
    ),
    "css": TreeSitterParser(
        "css",
        tree_sitter_css.language(),
    ),
    "json": TreeSitterParser(
        "json",
        tree_sitter_json.language(),
    ),
    "yaml": TreeSitterParser(
        "yaml",
        tree_sitter_yaml.language(),
    ),
}


def parser_for_language(language: str):
    return PARSERS.get(language)
