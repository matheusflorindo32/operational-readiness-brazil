import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_canonical_1484_ledger_passes_all_fail_closed_controls():
    subprocess.run([sys.executable, "analysis/audit_master_evidence_1484.py"], cwd=ROOT, check=True)
    result = json.loads(
        (ROOT / "batch10_4b" / "canonical" / "CANONICAL_COMPLETENESS_TEST.json").read_text(encoding="utf-8")
    )
    assert result["gate"] == "CANONICAL_1484_LEDGER_PASS"
    assert result["counts"] == {
        "rows": 1484,
        "unique_ids": 1484,
        "missing_ids": 0,
        "duplicate_ids": 0,
        "baseline": 1456,
        "additions": 28,
        "final_classifications_present": 1484,
        "provenance_present": 1484,
        "full_text_queue_reconciled": 285,
    }
    assert all(result["checks"].values())
