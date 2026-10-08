from dataclasses import dataclass
import re

from .models import FindingAction, FindingType


@dataclass(frozen=True)
class DetectionRule:
    rule_id: str
    finding_type: FindingType
    pattern: re.Pattern[str]
    confidence: float
    action: FindingAction
    reason: str


COMMENT_PREFIX = r"(?:#|//|/\*+|<!--|--)"


RULES = (
    DetectionRule(
        rule_id="ATTR-001",
        finding_type=FindingType.AI_ATTRIBUTION,
        pattern=re.compile(
            rf"^\s*{COMMENT_PREFIX}\s*"
            rf"(?:generated|created|written|built)\s+"
            rf"(?:by|with|using)\s+"
            rf"(?:chatgpt|claude|cursor|copilot|github copilot|"
            rf"v0|gemini|grok|codeium|windsurf)\b.*$",
            re.IGNORECASE,
        ),
        confidence=0.99,
        action=FindingAction.REMOVE,
        reason="Explicit attribution to an AI coding tool.",
    ),
    DetectionRule(
        rule_id="BANNER-001",
        finding_type=FindingType.GENERATED_BANNER,
        pattern=re.compile(
            rf"^\s*{COMMENT_PREFIX}\s*"
            rf"ai[- ]generated(?:\s+(?:code|file|component|project))?\s*$",
            re.IGNORECASE,
        ),
        confidence=0.98,
        action=FindingAction.REMOVE,
        reason="Explicit AI-generated banner.",
    ),
    DetectionRule(
        rule_id="NOTICE-001",
        finding_type=FindingType.TOOL_NOTICE,
        pattern=re.compile(
            rf"^\s*{COMMENT_PREFIX}\s*"
            rf"(?:this\s+)?(?:file|code|component)\s+"
            rf"(?:was\s+)?(?:generated|created|written)\s+"
            rf"(?:by|with|using)\s+"
            rf"(?:an?\s+)?(?:ai|llm|language model|"
            rf"chatgpt|claude|cursor|copilot|v0)\b.*$",
            re.IGNORECASE,
        ),
        confidence=0.97,
        action=FindingAction.REMOVE,
        reason="Explicit generated-code notice.",
    ),
    DetectionRule(
        rule_id="ASSIST-001",
        finding_type=FindingType.AI_ASSISTANT_MARKER,
        pattern=re.compile(
            rf"^\s*{COMMENT_PREFIX}\s*"
            rf"(?:assistant|ai assistant|coding assistant)\s*"
            rf"(?::|-)\s*"
            rf".+$",
            re.IGNORECASE,
        ),
        confidence=0.90,
        action=FindingAction.REVIEW,
        reason="Possible AI assistant marker requiring review.",
    ),
)
