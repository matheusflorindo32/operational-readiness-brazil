import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4b" / "ft5"
EXPECTED = {"EV-1462", "EV-1463", "EV-1466"}
CONTRADICTORY = {"EV-0052", "EV-0140", "EV-1066"}


def rows(name):
    with (OUT / name).open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def test_high22_scope_is_exact_and_excludes_appraised_high3():
    data = rows("HIGH22_ACCESS_REMEDIATION_MASTER.csv")
    ids = {row["Evidence_ID"] for row in data}
    assert len(data) == 22
    assert len(ids) == 22
    assert not ids & EXPECTED
    assert CONTRADICTORY <= ids
    assert all(row["Final_Access_Status"] for row in data)


def test_only_validated_bodies_are_appraisal_ready_and_unique():
    data = rows("HIGH22_APPRAISAL_READINESS.csv")
    ready = [row for row in data if row["Appraisal_Ready"] == "YES"]
    assert len(data) == 22
    assert all(all(row[key] == "YES" for key in ("Methods", "Results", "Discussion", "References")) for row in ready)
    assert all(row["No_Shared_Unrelated_Source"] == "YES" for row in data)


def test_access_statuses_do_not_overstate_transport_or_rate_limit_failures():
    data = rows("HIGH22_ACCESS_REMEDIATION_MASTER.csv")
    allowed = {"FULL_TEXT_RECOVERED_FINAL_VERSION", "FULL_TEXT_RECOVERED_ACCEPTED_MANUSCRIPT", "FULL_TEXT_RECOVERED_AUTHOR_MANUSCRIPT", "FULL_TEXT_RECOVERED_PREPRINT_ONLY", "FULL_TEXT_RECOVERED_OTHER_LAWFUL_VERSION", "ABSTRACT_ONLY", "PAYWALLED_NO_LAWFUL_FULL_TEXT_FOUND", "FULL_TEXT_ROUTE_BROKEN", "IDENTITY_CONFLICT", "ACCESS_UNRESOLVED"}
    assert {row["Final_Access_Status"] for row in data} <= allowed


def test_manifest_preserves_non_mutation_controls():
    manifest = json.loads((OUT / "BATCH10_4B_FT5_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["processed"] == 22
    assert manifest["cef_v1"] == manifest["zotero"] == manifest["manuscript"] == "UNCHANGED"
