import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_source_discovery_keeps_batch10_4b_fail_closed():
    subprocess.run([sys.executable, "analysis/audit_batch10_4b_source_discovery.py"], cwd=ROOT, check=True)
    report = json.loads((ROOT / "batch10_4b" / "scientific" / "BATCH10_4B_SOURCE_DISCOVERY_AUDIT.json").read_text(encoding="utf-8"))
    assert report["counts"] == {
        "queue": 285,
        "unique_evidence_ids": 285,
        "lawful_pmc_xml": 100,
        "full_text_unavailable": 185,
        "contradictory": 3,
        "replacement": 16,
        "final_includes": 0,
    }
    assert report["gate"] == "PARTIAL_GO"
    assert all(report["checks"].values())
