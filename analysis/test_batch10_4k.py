import csv
import hashlib
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4k"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def rows(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_final_reference_freeze_controls_pass():
    manifest = json.loads((OUT / "BATCH10_4K_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["gate"] == "FINAL_REFERENCE_FREEZE_PASS"
    assert manifest["active_claims"] == 10 and manifest["empirical_occurrences"] == 13
    assert manifest["international_references"] == 4 and manifest["brazil_references"] == 9
    assert manifest["shared_references"] == 3 and manifest["total_unique_references"] == 10
    for key in ["unsupported_active_claims", "empirical_claim_without_result_id", "result_id_without_locator", "citation_without_reference", "reference_without_citation", "orphan_reference", "duplicate_doi", "conflicting_identity", "rejected_pmcid_reuse", "cohort_double_counting", "null_result_suppression", "contradictory_high_used_as_support", "CEF_v1_unauthorized_change", "Zotero_changed", "scientific_claims_changed", "result_ids_changed"]:
        assert manifest[key] == 0


def test_references_chains_and_numbering_reconcile():
    chains = rows("FINAL_CLAIM_RESULT_REFERENCE_CHAIN.csv")
    assert len(chains) == 13
    assert {row["Final_Chain_Status"] for row in chains} == {"PASS"}
    for name, expected in [("INTERNATIONAL_FINAL_REFERENCE_SET.csv", 4), ("BRAZIL_FINAL_REFERENCE_SET.csv", 9)]:
        references = rows(name)
        assert len(references) == expected
        assert [int(row["Citation_Number"]) for row in references] == list(range(1, expected + 1))
        assert len({row["DOI"].casefold() for row in references}) == expected
    orphan = rows("FINAL_REFERENCE_ORPHAN_AUDIT.csv")
    assert all(row["Citation_Only"] == row["Bibliography_Only"] == row["Orphan_References"] == "0" for row in orphan)


def test_rejected_pmcid_is_not_reused_and_nulls_cohort_are_preserved():
    identifiers = rows("FINAL_DOI_PMID_PMCID_AUDIT.csv")
    ev1474 = next(row for row in identifiers if row["Evidence_ID"] == "EV-1474")
    assert ev1474["PMCID_Active"] == "NR"
    assert ev1474["Rejected_PMCID"] == "PMC3382270"
    assert ev1474["PMCID_Status"] == "REJECTED_LEGACY_PMCID_NOT_REUSED"
    assert all(row["Null_Result_Preserved"] == "YES" for row in rows("FINAL_NULL_RESULT_POST_FREEZE_AUDIT.csv"))
    cohort = rows("FINAL_COHORT_POST_FREEZE_AUDIT.csv")[0]
    assert cohort["Independent_Cohort_Count"] == "1" and cohort["Double_Counting"] == "0"


def test_frozen_docx_and_required_hashes_are_valid():
    hashes = json.loads((OUT / "FINAL_REFERENCE_FREEZE_HASHES.json").read_text(encoding="utf-8"))["sha256"]
    for name in ["International_v0.16-B2-SCIENTIFIC-FROZEN.docx", "Brazil_v0.16-B2-SCIENTIFIC-FROZEN.docx"]:
        path = OUT / name
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
            root = ET.fromstring(archive.read("word/document.xml"))
            text = "".join(node.text or "" for node in root.findall(".//w:t", NS))
            assert "DOI:" in text
        assert hashes[name] == hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = OUT / "BATCH10_4K_MANIFEST.json"
    assert hashes[manifest.name] == hashlib.sha256(manifest.read_bytes()).hexdigest()
