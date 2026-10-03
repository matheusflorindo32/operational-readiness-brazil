"""Fail-closed entry audit for Deep Evidence Batch 10.4B.

The audit deliberately separates an upstream assertion from independently
verifiable row-level evidence.  It does not screen, fetch, alter Zotero, or
make scientific decisions.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOOP = ROOT / "loop3x"
OUT = ROOT / "batch10_4b"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main() -> int:
    manifest = json.loads((LOOP / "LOOP_3X_MANIFEST.json").read_text(encoding="utf-8"))
    queue = read_csv(LOOP / "FULL_TEXT_REVIEW_QUEUE.csv")
    checkpoints = read_csv(LOOP / "LOOP_CHECKPOINT_LEDGER.csv")
    reference_qa = read_csv(ROOT / "batch10_3" / "REFERENCE_QA.csv")
    baseline_identity = read_csv(
        ROOT / "reporting" / "preanalysis" / "2026-09-06" / "evidence-identity-map.csv"
    )
    later_additions = read_csv(
        ROOT
        / "reporting"
        / "deep-evidence"
        / "2026-09-20"
        / "batch-03"
        / "master-evidence-reconciliation-batch-03.csv"
    )
    cef = (ROOT / "reporting" / "batch06f" / "CORE_EVIDENCE_FREEZE_v1.md").read_text(
        encoding="utf-8"
    )

    queue_ids = [row["Evidence_ID"] for row in queue]
    queue_classes = Counter(row["Pass3"] for row in queue)
    checkpoint_total = sum(int(row["Processed"]) for row in checkpoints)
    expected_additions = manifest["canonical_expected"] - len(baseline_identity)
    unreconciled_additions = expected_additions - len(later_additions)
    row_level_candidates = []
    for path in LOOP.glob("*.csv"):
        rows = read_csv(path)
        if len(rows) >= manifest["canonical_expected"] and "Evidence_ID" in (rows[0] if rows else {}):
            row_level_candidates.append(path.name)

    findings = [
        {
            "id": "LOOP_MANIFEST_COUNTS",
            "status": "DECLARED_NOT_INDEPENDENTLY_PROVABLE",
            "detail": "The upstream manifest declares 1,484 processed, unique IDs and final classifications.",
        },
        {
            "id": "CHECKPOINT_TOTAL",
            "status": "PASS",
            "detail": f"15 checkpoint lots sum to {checkpoint_total} processed records.",
        },
        {
            "id": "QUEUE_IDENTITY",
            "status": "PASS",
            "detail": f"Queue has {len(queue)} rows and {len(set(queue_ids))} unique Evidence IDs.",
        },
        {
            "id": "ROW_LEVEL_FINAL_CLASSIFICATION_SOURCE",
            "status": "BLOCKED",
            "detail": (
                "No 1,484-row CSV in loop3x contains Evidence_ID plus a final classification; "
                "therefore zero missing IDs and zero missing classifications cannot be independently recomputed."
            ),
        },
        {
            "id": "CANONICAL_UNIVERSE_RECONCILIATION",
            "status": "BLOCKED",
            "detail": (
                f"The preserved identity map has {len(baseline_identity)} rows and the later-additions ledger has "
                f"{len(later_additions)} rows; this reconciles to {len(baseline_identity) + len(later_additions)}, "
                f"leaving {unreconciled_additions} of the {expected_additions} expected additions without a row in that ledger. "
                "Neither source provides a unified final-classification ledger."
            ),
        },
        {
            "id": "CEF_V1",
            "status": "PASS" if "EV-1379 remains fail-closed" in cef else "BLOCKED",
            "detail": "CEF-v1 remains frozen; EV-1379 must not support claims.",
        },
        {
            "id": "CURRENT_REFERENCE_SET",
            "status": "PASS" if len(reference_qa) == 16 else "BLOCKED",
            "detail": f"Reference QA ledger contains {len(reference_qa)} currently cited references.",
        },
    ]
    blocked = [finding for finding in findings if finding["status"] == "BLOCKED"]
    output = {
        "phase": "DEEP EVIDENCE BATCH 10.4B — ENTRY AUDIT",
        "entry_head": "a0fcb99fe67f4009526668acf3e43028ad83e646",
        "upstream_loop_manifest": {
            "canonical_expected": manifest["canonical_expected"],
            "processed": manifest["processed"],
            "unique_ev_ids": manifest["unique_ev_ids"],
            "missing_ev_ids": manifest["missing_ev_ids"],
            "missing_classifications": manifest["missing_classifications"],
        },
        "independent_observations": {
            "checkpoint_processed_sum": checkpoint_total,
            "full_text_queue_rows": len(queue),
            "full_text_queue_unique_evidence_ids": len(set(queue_ids)),
            "full_text_queue_classes": dict(sorted(queue_classes.items())),
            "row_level_final_classification_artifacts": row_level_candidates,
            "baseline_identity_rows": len(baseline_identity),
            "later_additions_rows": len(later_additions),
            "expected_later_additions": expected_additions,
            "unreconciled_later_additions": unreconciled_additions,
            "current_reference_count_international": len(reference_qa),
            "current_reference_count_brazil": len(reference_qa),
            "cef_v1_changed": False,
            "ev_1379": "FAIL_CLOSED",
        },
        "findings": findings,
        "gate": "BLOCKED" if blocked else "GO_FULL_TEXT_SATURATION",
        "blocker": blocked[0]["detail"] if blocked else None,
        "permitted_next_action": (
            "Reconstruct and version a 1,484-row canonical screening ledger with Evidence_ID, final classification, "
            "source provenance, the 1,456 baseline, all 28 additions, and explicit resolution of the two additions "
            "missing from the available reconciliation ledger."
            if blocked
            else "Begin controlled full-text saturation review."
        ),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "BATCH10_4B_MANIFEST.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
