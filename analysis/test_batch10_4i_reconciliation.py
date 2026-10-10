import csv
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "batch10_4h_r"
OUT = ROOT / "batch10_4i"


def read_csv(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_final_audit_is_complete_and_non_destructive():
    manifest = json.loads((OUT / "BATCH10_4I_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["gate"] == "V015_FINAL_SCIENTIFIC_AUDIT_PASS"
    assert manifest["retained_claims_audited"] == 10
    assert manifest["claim_occurrences_audited"] == manifest["claim_chains_pass"] == 13
    assert manifest["removed_claims_reintroduced"] == 0
    assert manifest["contradictory_support_use"] == 0
    assert manifest["orphan_references"] == manifest["duplicate_doi"] == 0
    assert manifest["cohort_double_counting"] == 0
    assert manifest["reference_freeze_executed"] == manifest["Zotero_changed"] == manifest["CEF_v1_changed"] == 0
    assert manifest["v015_content_changed"] == 0


def test_all_empirical_claim_chains_and_reference_sets_reconcile():
    chains = read_csv("FINAL_V015_CLAIM_RESULT_LOCATOR_CHAIN.csv")
    assert len(chains) == 13
    assert {row["Chain_Status"] for row in chains} == {"PASS"}
    orphans = read_csv("FINAL_V015_ORPHAN_REFERENCE_AUDIT.csv")
    assert len(orphans) == 2
    for row in orphans:
        assert row["Cited_But_Not_Listed"] == row["Listed_But_Not_Cited"] == "0"
        assert row["Duplicate_DOIs"] == row["Invalid_Placeholders"] == "0"
        assert row["Audit_Status"] == "PASS"


def test_only_material_human_decisions_remain_and_docx_are_valid():
    queue = read_csv("FINAL_V015_HUMAN_REVIEW_QUEUE.csv")
    assert len(queue) == 2
    assert {row["Item_Type"] for row in queue} == {"MANUSCRIPT_VIABILITY"}
    assert all(not row["HUMAN_DECISION"] and not row["HUMAN_REVIEWER"] for row in queue)
    for name in ["International_v0.15-B2-EVIDENCE-FIRST.docx", "Brazil_v0.15-B2-EVIDENCE-FIRST.docx"]:
        with zipfile.ZipFile(PKG / name) as archive:
            assert archive.testzip() is None
            assert "word/document.xml" in archive.namelist()
