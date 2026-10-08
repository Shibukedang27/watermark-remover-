import json
from pathlib import Path

from codecleaner.classification.engine import ClassificationEngine
from codecleaner.classification.report import write_report

from .test_classification_engine import make_finding


def test_report_written(tmp_path: Path):
    engine = ClassificationEngine()

    findings = engine.classify_many([
        make_finding(),
        make_finding(confidence=0.90),
    ])

    summary = engine.summarize(findings)

    output = tmp_path / "report.json"

    write_report(output, findings, summary)

    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["version"] == "1.0"
    assert data["summary"]["total"] == 2
    assert len(data["findings"]) == 2
