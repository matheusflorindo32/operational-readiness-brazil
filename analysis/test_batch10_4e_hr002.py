import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def test_hr002_is_the_only_new_official_queue_decision():
    queue = rows(ROOT / "batch10_4d" / "FINAL_HUMAN_REVIEW_QUEUE.csv")
    target = next(row for row in queue if row["Review_ID"] == "HR-002")
    assert target["HUMAN_DECISION"] == "MAINTAIN"
    assert target["HUMAN_REVIEWER"] == "Matheus Florindo de Deus"
    assert target["HUMAN_REVIEW_DATE"] == "2026-10-06"
    for row in queue:
        if row["Review_ID"] not in {"HR-002", "HR-003", "HR-004", "HR-005", "HR-006", "HR-007", "HR-008", "HR-009"}:
            assert not row["HUMAN_DECISION"] and not row["HUMAN_REVIEWER"] and not row["HUMAN_REVIEW_DATE"] and not row["HUMAN_RATIONALE"]

def test_hr002_manuscript_controls_are_fail_closed():
    audited = rows(ROOT / "batch10_4e" / "HR002_MANUSCRIPT_COMPLIANCE_AUDIT.csv")
    assert len(audited) == 2
    for row in audited:
        assert row["EV0052_Used_As_Support"] == "NO"
        assert row["Definitive_Prediction_Claim"] == "NO"
        assert row["Unsupported_Causal_Statement"] == "NO"
        assert row["Limitation_Preserved"] == "YES"
        assert row["Overclaim_Status"] == "PASS_AS_WRITTEN"
        assert row["FCR_Candidate"] == "NO"

def test_no_v014_and_only_authorized_decision_recorded():
    assert not list(ROOT.rglob("*v0.14*"))
    decision = rows(ROOT / "batch10_4e" / "HR002_HUMAN_DECISION_RECORD.csv")
    assert len(decision) == 1 and decision[0]["Review_ID"] == "HR-002" and decision[0]["HUMAN_DECISION"] == "MAINTAIN"
