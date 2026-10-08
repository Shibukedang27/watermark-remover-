from pathlib import Path

from codecleaner.features.models import FileFeatures
from codecleaner.patterns import (
    ArtifactSeverity,
    PatternCategory,
    PatternScoringEngine,
)


def features(**overrides):
    values = {
        "file": "example.py",
        "total_lines": 100,
        "code_lines": 70,
        "comment_lines": 20,
        "blank_lines": 10,
        "comment_ratio": 0.20,
        "blank_line_ratio": 0.10,
        "comment_repetition": 0.0,
        "duplicate_line_ratio": 0.0,
        "duplicate_block_signal": 0.0,
        "boilerplate_density": 0.0,
        "generated_phrase_density": 0.0,
        "code_density": 0.70,
    }
    values.update(overrides)
    return FileFeatures(**values)


def test_clean_file_has_low_score():
    result = PatternScoringEngine().score_file(features())

    assert result.score == 0.0
    assert result.confidence == 0.0
    assert result.severity == ArtifactSeverity.LOW
    assert result.matches == ()
    assert "No significant" in result.explanation


def test_generated_attribution_is_detected():
    result = PatternScoringEngine().score_file(
        features(generated_phrase_density=0.50)
    )

    assert result.score > 0
    assert result.matches
    assert result.matches[0].category == PatternCategory.GENERATED_ATTRIBUTION
    assert result.matches[0].signal == "generated_phrase_density"


def test_multiple_signals_increase_score_and_confidence():
    result = PatternScoringEngine().score_file(
        features(
            generated_phrase_density=0.60,
            boilerplate_density=0.50,
            comment_repetition=0.50,
            duplicate_line_ratio=0.30,
            duplicate_block_signal=0.30,
        )
    )

    assert result.score > 0.40
    assert result.confidence > 0.90
    assert result.severity in {
        ArtifactSeverity.MEDIUM,
        ArtifactSeverity.HIGH,
        ArtifactSeverity.VERY_HIGH,
    }
    assert len(result.matches) >= 4


def test_score_is_bounded():
    result = PatternScoringEngine().score_file(
        features(
            generated_phrase_density=1.0,
            boilerplate_density=1.0,
            comment_repetition=1.0,
            duplicate_line_ratio=1.0,
            duplicate_block_signal=1.0,
            blank_line_ratio=1.0,
        )
    )

    assert 0.0 <= result.score <= 1.0
    assert 0.0 <= result.confidence <= 1.0


def test_thresholds_ignore_weak_signals():
    result = PatternScoringEngine().score_file(
        features(
            generated_phrase_density=0.001,
            boilerplate_density=0.01,
            comment_repetition=0.02,
            duplicate_line_ratio=0.01,
            duplicate_block_signal=0.01,
            blank_line_ratio=0.20,
        )
    )

    assert result.matches == ()
    assert result.score == 0.0


def test_project_scoring_preserves_order():
    engine = PatternScoringEngine()

    items = (
        features(file="a.py", generated_phrase_density=0.2),
        features(file="b.py", comment_repetition=0.4),
    )

    results = engine.score_project(items)

    assert [item.file for item in results] == ["a.py", "b.py"]
    assert results[0].score > 0
    assert results[1].score > 0


def test_to_dict_is_serializable():
    result = PatternScoringEngine().score_file(
        features(
            generated_phrase_density=0.4,
            boilerplate_density=0.3,
        )
    )

    payload = result.to_dict()

    assert payload["file"] == "example.py"
    assert isinstance(payload["matches"], list)
    assert payload["severity"] in {
        "low",
        "medium",
        "high",
        "very_high",
    }


def test_duplicate_code_signal():
    result = PatternScoringEngine().score_file(
        features(duplicate_line_ratio=0.50)
    )

    assert any(
        item.category == PatternCategory.DUPLICATE_CODE
        for item in result.matches
    )


def test_duplicate_block_signal():
    result = PatternScoringEngine().score_file(
        features(duplicate_block_signal=0.50)
    )

    assert any(
        item.category == PatternCategory.DUPLICATE_BLOCKS
        for item in result.matches
    )
