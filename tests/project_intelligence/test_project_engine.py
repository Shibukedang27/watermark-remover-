import pytest

from codecleaner.patterns.models import ArtifactScore, ArtifactSeverity
from codecleaner.project_intelligence import (
    ProjectIntelligence,
    ProjectSeverity,
)


def score(file, value):
    return ArtifactScore(
        file=file,
        score=value,
        confidence=min(1.0, value + 0.4),
        severity=(
            ArtifactSeverity.VERY_HIGH
            if value >= 0.8
            else ArtifactSeverity.HIGH
            if value >= 0.6
            else ArtifactSeverity.MEDIUM
            if value >= 0.3
            else ArtifactSeverity.LOW
        ),
        matches=(),
        explanation="test",
    )


def test_empty_project_is_clean():
    result = ProjectIntelligence().analyze([], total_files=3)

    assert result.severity == ProjectSeverity.CLEAN
    assert result.analyzed_files == 0
    assert result.average_score == 0.0


def test_project_aggregates_files():
    result = ProjectIntelligence().analyze(
        [
            score("a.py", 0.7),
            score("b.py", 0.8),
            score("c.py", 0.1),
        ]
    )

    assert result.average_score > 0
    assert result.maximum_score == 0.8
    assert result.high_risk_files == 2
    assert result.very_high_risk_files == 1
    assert result.concentration == pytest.approx(2 / 3, abs=1e-6)
    assert result.severity in {
        ProjectSeverity.MEDIUM,
        ProjectSeverity.HIGH,
        ProjectSeverity.VERY_HIGH,
    }


def test_project_dict():
    result = ProjectIntelligence().analyze([score("a.py", 0.7)])

    payload = result.to_dict()

    assert payload["total_files"] == 1
    assert payload["severity"] in {
        "medium",
        "high",
        "very_high",
    }
