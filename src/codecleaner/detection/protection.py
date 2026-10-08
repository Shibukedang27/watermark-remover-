from dataclasses import dataclass


@dataclass(frozen=True)
class ProtectionDecision:
    protected: bool
    reason: str | None = None


PROTECTED_PATTERNS = (
    "copyright",
    "licensed under",
    "license",
    "spdx-license-identifier",
    "apache license",
    "mit license",
    "gnu general public license",
    "mozilla public license",
    "bsd license",
)


def protect_line(line: str) -> ProtectionDecision:
    lowered = line.lower()

    for pattern in PROTECTED_PATTERNS:
        if pattern in lowered:
            return ProtectionDecision(
                protected=True,
                reason=f"Possible legal or license notice: {pattern}",
            )

    return ProtectionDecision(protected=False)
