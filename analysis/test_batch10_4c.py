import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4c"


def rows(name):
    with (OUT / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def text(name):
    import zipfile
    from xml.etree import ElementTree as ET
    with zipfile.ZipFile(OUT / "manuscripts" / name) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    return "\n".join(node.text or "" for node in root.iter() if node.tag.endswith("}t"))


def test_outputs_exist_and_v012_is_not_versioned_as_output():
    assert (OUT / "manuscripts" / "International_v0.13-EVIDENCE-SATURATED.docx").exists()
    assert (OUT / "manuscripts" / "Brazil_v0.13-EVIDENCE-SATURATED.docx").exists()
    assert not (OUT / "manuscripts" / "International_v0.12-FULL-MANUSCRIPT.docx").exists()
    manifest = json.loads((OUT / "BATCH10_4C_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["v012"] == "UNCHANGED"
    assert len(manifest["source_sha256"]) == 2


def test_claims_and_limitations_are_complete():
    assert len(rows("V013_CLAIM_CITATION_MATRIX.csv")) == 60
    assert len(rows("V013_REQUIRED_LIMITATIONS_LEDGER.csv")) == 6
    assert all(r["International"] == "INSERTED" and r["Brazil"] == "INSERTED" for r in rows("V013_REQUIRED_LIMITATIONS_LEDGER.csv"))


def test_contradictions_access_and_framework_are_disclosed():
    for name in ["International_v0.13-EVIDENCE-SATURATED.docx", "Brazil_v0.13-EVIDENCE-SATURATED.docx"]:
        value = text(name)
        assert "EV-0052" in value and "EV-0140" in value and "EV-1066" in value
        assert "22" in value and "15" in value
        assert "PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED" in value
        assert "v0.13" in value
        assert "reverses sleep deprivation" not in value.lower()
        assert "caffeine solves sleep loss" not in value.lower()


def test_no_provisional_promotion_or_fcr_change():
    decisions = rows("V013_REFERENCE_DECISION_LEDGER.csv")
    assert all(r["Decision_v013"] == "NOT_PROMOTED_PENDING_HUMAN_REVIEW" for r in decisions)
    assert len(rows("V013_REPLACEMENT_DECISIONS.csv")) == 6
    manifest = json.loads((OUT / "BATCH10_4C_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["cef_v1"] == "UNCHANGED"
    assert manifest["zotero"] == "UNCHANGED"


def test_reference_list_remains_reconciled_to_verified_v012_set():
    for name in ["International_v0.13-EVIDENCE-SATURATED.docx", "Brazil_v0.13-EVIDENCE-SATURATED.docx"]:
        value = text(name).lower()
        assert value.count("doi:") == 15
        dois = [part.split()[0].rstrip(".") for part in value.split("doi:")[1:]]
        assert len(dois) == len(set(dois))
        assert "ev-1379" in value  # integrity hold is disclosed, never listed as support
    assert not any(r["Manuscript_Use"] != "NONE_AS_SUPPORT" for r in rows("V013_REFERENCE_DECISION_LEDGER.csv"))
