import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4b" / "ft1" / "artifacts"


def read_csv(name: str):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_ft1_lot01_is_bounded_and_fail_closed():
    manifest = json.loads((OUT / "BATCH10_4B_FT1_MANIFEST.json").read_text(encoding="utf-8"))
    decisions = read_csv("PMC100_PROVISIONAL_DECISIONS.csv")
    source = read_csv("PMC100_SOURCE_BODY_VALIDATION.csv")
    assert manifest["state"] == "PARTIAL_GO"
    assert manifest["reviewed"] == 10
    assert manifest["full_article_body_read"] == 9
    assert manifest["remaining"] == 90
    assert manifest["claim_ready_provisional"] == 0
    assert manifest["human_confirmation"] == 0
    assert manifest["cef_v1_changed"] is False
    assert manifest["ev_1379"] == "FAIL_CLOSED"
    assert len(decisions) == 10
    assert all(row["HUMAN_CONFIRMATION"] == "PENDING" for row in decisions)
    assert all(row["CLAIM_READY_PROVISIONAL"] == "NO" for row in decisions)
    assert len(source) == 100
    assert sum(row["FT1_Source_Body_Status"] == "FULL_ARTICLE_BODY_AVAILABLE" for row in source) == 85
    assert sum(row["FT1_Source_Body_Status"] == "XML_ABSTRACT_OR_FRAGMENT_ONLY" for row in source) == 15
