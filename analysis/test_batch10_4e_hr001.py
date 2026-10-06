import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4e"


def rows(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_hr001_statuses_are_complete_and_fail_closed():
    mapped = rows("HR001_CLAIM_SENTENCE_REFERENCE_MAP.csv")
    assert len(mapped) == 60
    allowed = {"MAPPED_CONFIRMED", "MAPPED_AFTER_NARROWING", "UNLINKED_NARROWING_REQUIRED", "UNLINKED_DELETE_REQUIRED", "AMBIGUOUS_HUMAN_REVIEW_REQUIRED"}
    assert all(row["Mapping_Status"] in allowed for row in mapped)
    assert all(row["Current_Citation"] == "NO_MANUSCRIPT_CITATION" for row in mapped)
    assert all(row["Reference_ID"] == "NOT_ASSIGNED_IN_V013" for row in mapped)
    assert all(row["Citation_Fit"] == "NO_SUPPORTING_CITATION_TO_ASSESS" for row in mapped)
    assert sum(row["Mapping_Status"] == "UNLINKED_DELETE_REQUIRED" for row in mapped) == 1


def test_hr001_decision_is_limited_to_authorized_row():
    decision = rows("HR001_HUMAN_DECISION_RECORD.csv")
    assert len(decision) == 1
    assert decision[0]["Review_ID"] == "HR-001"
    assert decision[0]["HUMAN_DECISION"] == "MAP MANUALLY"
    assert decision[0]["HUMAN_REVIEWER"] == "Matheus Florindo de Deus"
    queue = rows("../batch10_4d/FINAL_HUMAN_REVIEW_QUEUE.csv")
    assert all(not row["HUMAN_DECISION"] for row in queue if row["Review_ID"] not in {"HR-002", "HR-003", "HR-004"})
    assert all(not row["HUMAN_REVIEWER"] for row in queue if row["Review_ID"] not in {"HR-002", "HR-003", "HR-004"})
    assert all(not row["HUMAN_REVIEW_DATE"] for row in queue if row["Review_ID"] not in {"HR-002", "HR-003", "HR-004"})
    assert all(not row["HUMAN_RATIONALE"] for row in queue if row["Review_ID"] not in {"HR-002", "HR-003", "HR-004"})


def test_manifest_and_red_team_controls():
    manifest = json.loads((OUT / "HR001_MAPPING_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["claims_expected"] == manifest["claims_statused"] == 60
    assert manifest["blank_mapping_status"] == 0
    assert manifest["unsupported_forced_links"] == 0
    assert manifest["blocked_evidence_used_as_support"] == 0
    assert manifest["orphan_citations_created"] == 0
    assert manifest["cef_v1"] == manifest["zotero"] == "UNCHANGED"
    assert manifest["reference_freeze"] == "PROHIBITED_PENDING_HR002_TO_HR010"
