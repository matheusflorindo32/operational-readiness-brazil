import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4b" / "ft4"
EXPECTED = {"EV-1462", "EV-1463", "EV-1466"}


def read(name):
    with (OUT / name).open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def test_ft4_has_exactly_the_verified_three():
    rows = read("HIGH3_FULL_TEXT_EXTRACTION.csv")
    assert {row["Evidence_ID"] for row in rows} == EXPECTED
    assert len(rows) == 3
    assert len({row["Source_URL"] for row in rows}) == 3
    assert all(row["Full_text_sections_read"] and row["Methods_results"] for row in rows)


def test_appraisal_and_decisions_are_populated_and_conservative():
    appraisal = read("HIGH3_APPRAISAL_LEDGER.csv")
    decisions = read("HIGH3_PROVISIONAL_DECISIONS.csv")
    assert {row["Evidence_ID"] for row in appraisal} == EXPECTED
    assert {row["Evidence_ID"] for row in decisions} == EXPECTED
    assert all(row["Instrument"] and row["Overall_judgment"] for row in appraisal)
    assert all(row["Provisional_Decision"] and row["CLAIM_READY_PROVISIONAL"] == "NO" for row in decisions)
    assert all("FINAL" not in row["Provisional_Decision"] for row in decisions)


def test_manifest_retains_scope_and_non_mutation_controls():
    manifest = json.loads((OUT / "BATCH10_4B_FT4_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["processed_ids"] == sorted(EXPECTED)
    assert manifest["count"] == 3
    assert manifest["cef_v1"] == "UNCHANGED"
    assert manifest["zotero"] == "UNCHANGED"
    assert manifest["manuscript"] == "UNCHANGED"
