import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    name: str
    category: str
    pattern: re.Pattern
    confidence: float
    reason: str


RULES = [
    Rule(
        "generated_by_ai_tool",
        "ai_attribution",
        re.compile(
            r"^\s*(?://|#|/\*+|<!--|--)\s*"
            r"(?:generated|created|written|built)\s+"
            r"(?:by|with|using)\s+"
            r"(?:chatgpt|claude|cursor|copilot|github copilot|v0|gemini|grok)\b.*$",
            re.IGNORECASE,
        ),
        0.99,
        "Explicit AI/tool attribution marker.",
    ),
    Rule(
        "ai_generated_banner",
        "generated_banner",
        re.compile(
            r"^\s*(?://|#|/\*+|<!--|--)\s*"
            r"ai[- ]generated\s*(?:code|file|component)?\s*$",
            re.IGNORECASE,
        ),
        0.98,
        "Explicit AI-generated banner.",
    ),
]


def classify_line(line: str):
    for rule in RULES:
        if rule.pattern.match(line):
            return rule
    return None


def is_legal_or_copyright_notice(line: str) -> bool:
    lowered = line.lower()

    protected = (
        "copyright",
        "licensed under",
        "license",
        "spdx-license-identifier",
        "apache license",
        "mit license",
        "gnu general public license",
        "gpl-",
        "bsd license",
    )

    return any(token in lowered for token in protected)
