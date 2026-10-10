import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "batch10_4i"
OUT = ROOT / "batch10_4j"


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_final_human_adjudication_is_complete_and_limited_to_article_strategy():
    manifest = json.loads((OUT / "BATCH10_4J_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["gate"] == "FINAL_HUMAN_ADJUDICATION_PASS"
    assert manifest["human_decisions_expected"] == manifest["human_decisions_completed"] == 2
    assert manifest["simulated_human_decisions"] == manifest["unresolved_material_human_decisions"] == 0
    assert manifest["scientific_claims_changed"] == manifest["result_ids_changed"] == 0
    assert manifest["evidence_roles_changed"] == manifest["null_findings_changed"] == 0
    assert manifest["CEF_v1_changed"] == manifest["Zotero_changed"] == 0
    assert manifest["references_frozen"] is False
    assert manifest["freeze_readiness"] == "READY_FOR_FINAL_REFERENCE_FREEZE"


def test_official_queue_matches_the_explicit_user_decisions():
    queue = rows(AUDIT / "FINAL_V015_HUMAN_REVIEW_QUEUE.csv")
    expected = {
        "V015-INT-ARTICLE-STRATEGY": "APPROVE_SHORT_FORM",
        "V015-BRA-ARTICLE-STRATEGY": "APPROVE_SHORT_FORM",
    }
    assert {row["Review_ID"]: row["HUMAN_DECISION"] for row in queue} == expected
    assert all(row["HUMAN_REVIEWER"] == "Matheus Florindo de Deus" for row in queue)
    assert all(row["HUMAN_REVIEW_DATE"] == "2026-10-09" for row in queue)


def test_freeze_remains_not_executed():
    readiness = rows(OUT / "POST_HUMAN_FINAL_FREEZE_READINESS.csv")
    values = {row["Control"]: row["Observed"] for row in readiness}
    assert values["References frozen"] == "NO"
    assert values["Freeze readiness"] == "READY_FOR_FINAL_REFERENCE_FREEZE"
