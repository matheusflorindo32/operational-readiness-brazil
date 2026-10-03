import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_entry_audit_releases_only_with_complete_canonical_ledger():
    subprocess.run([sys.executable, "analysis/audit_batch10_4b_entry.py"], cwd=ROOT, check=True)
    manifest = json.loads((ROOT / "batch10_4b" / "BATCH10_4B_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["gate"] == "GO_FULL_TEXT_SATURATION_REVIEW"
    assert manifest["independent_observations"]["checkpoint_processed_sum"] == 1484
    assert manifest["independent_observations"]["full_text_queue_rows"] == 285
    assert manifest["independent_observations"]["full_text_queue_unique_evidence_ids"] == 285
    assert manifest["independent_observations"]["canonical_ledger_rows"] == 1484
    assert manifest["independent_observations"]["row_level_final_classification_artifacts"] == [
        "batch10_4b/canonical/MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv"
    ]
    assert manifest["independent_observations"]["baseline_identity_rows"] == 1456
    assert manifest["independent_observations"]["later_additions_rows"] == 26
    assert manifest["independent_observations"]["expected_later_additions"] == 28
    assert manifest["independent_observations"]["unreconciled_later_additions"] == 2
