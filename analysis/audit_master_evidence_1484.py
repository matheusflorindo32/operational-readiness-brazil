"""Fail-closed audit for the canonical 1,484-record reconciliation artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "batch10_4b" / "canonical"
LEDGER = CANONICAL / "MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    rows = read_csv(LEDGER)
    ids = [row["Evidence_ID"] for row in rows]
    expected = [f"EV-{index:04d}" for index in range(1, 1485)]
    classes = Counter(row["LOOP3X_Final_Class"] for row in rows)
    baseline = [row for row in rows if row["Baseline_or_Addition"] == "BASELINE"]
    additions = [row for row in rows if row["Baseline_or_Addition"] == "ADDITION"]
    queue = read_csv(ROOT / "loop3x" / "FULL_TEXT_REVIEW_QUEUE.csv")
    queue_ids = {row["Evidence_ID"] for row in queue}
    canonical_by_id = {row["Evidence_ID"]: row for row in rows}
    cef = (ROOT / "reporting" / "batch06f" / "CORE_EVIDENCE_FREEZE_v1.md").read_text(encoding="utf-8")
    checks = {
        "row_count": len(rows) == 1484,
        "unique_ids": len(set(ids)) == 1484,
        "first_id": ids[0] == "EV-0001",
        "last_id": ids[-1] == "EV-1484",
        "complete_sequence": ids == expected,
        "baseline_count": len(baseline) == 1456,
        "addition_count": len(additions) == 28,
        "final_classifications_present": all(row["LOOP3X_Final_Class"] for row in rows),
        "source_and_provenance_present": all(row["Canonical_Source"] and row["Provenance"] for row in rows),
        "queue_reconciled": len(queue) == 285 and all(item in canonical_by_id for item in queue_ids),
        "full_text_class_count": classes["FULL_TEXT_REVIEW"] == 266,
        "replace_class_count": classes["REPLACE_EXISTING_CANDIDATE"] == 16,
        "contradictory_class_count": classes["CONTRADICTORY_CANDIDATE"] == 3,
        "ev_1379_fail_closed": canonical_by_id["EV-1379"]["LOOP3X_Final_Class"] == "INTEGRITY_BLOCK"
        and "EV-1379 remains fail-closed" in cef,
        "cef_v1_intact": all(token in cef for token in ("## Core", "## Supporting", "## Contextual", "## Hold integrity")),
    }
    result = {
        "phase": "BATCH 10.4B-R CANONICAL LEDGER AUDIT",
        "canonical_ledger": str(LEDGER.relative_to(ROOT)).replace("\\", "/"),
        "canonical_ledger_sha256": sha256(LEDGER),
        "counts": {
            "rows": len(rows), "unique_ids": len(set(ids)), "missing_ids": len(set(expected) - set(ids)),
            "duplicate_ids": len(ids) - len(set(ids)), "baseline": len(baseline), "additions": len(additions),
            "final_classifications_present": sum(bool(row["LOOP3X_Final_Class"]) for row in rows),
            "provenance_present": sum(bool(row["Canonical_Source"] and row["Provenance"]) for row in rows),
            "full_text_queue_reconciled": sum(item in canonical_by_id for item in queue_ids),
        },
        "final_classes": dict(sorted(classes.items())),
        "checks": checks,
        "gate": "CANONICAL_1484_LEDGER_PASS" if all(checks.values()) else "CANONICAL_1484_LEDGER_BLOCKED",
    }
    (CANONICAL / "CANONICAL_COMPLETENESS_TEST.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
