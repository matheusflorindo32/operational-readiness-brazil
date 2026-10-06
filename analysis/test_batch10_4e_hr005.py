import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def test_hr005_only_authorized_queue_update():
    queue = rows(ROOT / "batch10_4d" / "FINAL_HUMAN_REVIEW_QUEUE.csv")
    target = next(row for row in queue if row["Review_ID"] == "HR-005")
    assert target["HUMAN_DECISION"] == "KEEP_CURRENT"
    assert target["HUMAN_REVIEWER"] == "Matheus Florindo de Deus"
    assert target["HUMAN_REVIEW_DATE"] == "2026-10-06"
    assert all(not row["HUMAN_DECISION"] for row in queue if row["Review_ID"] in {"HR-007", "HR-008", "HR-009", "HR-010"})

def test_hr005_comparison_and_claim_boundaries():
    comparison = rows(ROOT / "batch10_4e" / "HR005_REPLACEMENT_COMPARISON.csv")
    assert len(comparison) == 18
    assert {row["Dimension_Number"] for row in comparison} == {str(i) for i in range(1, 19)}
    assert {row["Final_Classification"] for row in comparison} == {"KEEP_CURRENT"}
    impact = rows(ROOT / "batch10_4e" / "HR005_CLAIM_IMPACT.csv")
    supplement = next(row for row in impact if row["Claim_ID"] == "INT-MED-CAUTIOUS-SUPPLEMENT")
    assert supplement["Current_Wording"] == "NOT PRESENT AS A SUPPORTING CLAIM IN V0.13."
    assert "no statistically or clinically significant" in supplement["EV0386_Role"]

def test_hr005_no_freeze_or_unapproved_promotion():
    record = rows(ROOT / "batch10_4e" / "HR005_HUMAN_DECISION_RECORD.csv")[0]
    assert record["Final_Classification"] == "KEEP_CURRENT"
    assert record["Final_Reference_Freeze"] == "NO"
    assert "Not promoted" in record["EV0386_Use"]
    manifest = json.loads((ROOT / "batch10_4d" / "BATCH10_4D_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["human_adjudication_updates"]["HR-005"]["decision"] == "KEEP_CURRENT"
