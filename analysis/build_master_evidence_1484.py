"""Materialize the canonical 1,484-row LOOP 3x ledger from its Drive export.

The input is an exported *read-only* Google Sheet.  This script does not alter
the sheet, Zotero, the CEF, screening classes, or manuscript content.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import openpyxl


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4b" / "canonical"
SOURCE_FILE_ID = "1PsCIFKpNMjrpsaHVu2mGKFYlRboKvNGgorZocCILnoY"
SOURCE_VERSION = "Drive modified 2026-09-21T02:35:49.190Z"
SOURCE_URL = f"https://docs.google.com/spreadsheets/d/{SOURCE_FILE_ID}/edit"

FIELDS = [
    "Evidence_ID", "Title", "DOI", "PMID", "PMCID", "Zotero_Key", "Year", "Country",
    "Population", "Study_Design", "Canonical_Status", "Canonical_Source",
    "Canonical_Source_File", "Canonical_Source_Version", "Canonicalization_Batch",
    "Provenance", "Baseline_or_Addition", "Addition_Number", "LOOP3X_Pass1",
    "LOOP3X_Pass2", "LOOP3X_Final_Class", "LOOP3X_Priority", "Domain",
    "Manuscript_Layer", "Section", "Full_Text_Required", "Contradictory_Flag",
    "Replace_Existing_Flag", "Integrity_Status", "Freeze_Change_Candidate",
    "Overlap_Family", "Human_Review_Status", "Notes",
]


def clean(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def additions() -> dict[str, dict[str, str]]:
    known = {
        row["canonical_evidence_id"]: row
        for row in read_csv(
            ROOT / "reporting" / "deep-evidence" / "2026-09-20" / "batch-03"
            / "master-evidence-reconciliation-batch-03.csv"
        )
    }
    known["EV-1483"] = {
        "provenance": "Batch05 exact PMID/DOI/title reconciliation; BATCH05_AUDIT.md",
        "reconciliation_result": "CANONICAL_ID_ASSIGNED; ZOTERO_WRITE_PENDING",
    }
    known["EV-1484"] = {
        "provenance": "Batch05 exact PMID/DOI/title reconciliation; BATCH05_AUDIT.md",
        "reconciliation_result": "CANONICAL_ID_ASSIGNED; ZOTERO_WRITE_PENDING",
    }
    return known


def source_value(row: tuple[object, ...], indexes: dict[str, int], name: str) -> str:
    return clean(row[indexes[name]]) if name in indexes else ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="Drive-exported LOOP 3x XLSX")
    args = parser.parse_args()
    book = openpyxl.load_workbook(args.input, read_only=True, data_only=True)
    sheet = book["FULL_UNIVERSE_SCREENING"]
    rows = sheet.iter_rows(values_only=True)
    next(rows)
    next(rows)
    headers = [clean(value) for value in next(rows)]
    indexes = {name: index for index, name in enumerate(headers) if name}
    canonical_additions = additions()
    materialized: list[dict[str, str]] = []

    for raw in rows:
        evidence_id = source_value(raw, indexes, "Evidence ID")
        if not evidence_id:
            continue
        ordinal = int(evidence_id.removeprefix("EV-"))
        is_baseline = ordinal <= 1456
        addition = canonical_additions.get(evidence_id, {})
        materialized.append({
            "Evidence_ID": evidence_id,
            "Title": source_value(raw, indexes, "Title"),
            "DOI": source_value(raw, indexes, "Normalized DOI") or source_value(raw, indexes, "DOI"),
            "PMID": source_value(raw, indexes, "PMID"),
            "PMCID": source_value(raw, indexes, "PMCID"),
            "Zotero_Key": source_value(raw, indexes, "Zotero Item Key"),
            "Year": source_value(raw, indexes, "Year"),
            "Country": source_value(raw, indexes, "Country"),
            "Population": source_value(raw, indexes, "Occupation / Population"),
            "Study_Design": source_value(raw, indexes, "Study Design"),
            "Canonical_Status": "CANONICAL_BASELINE" if is_baseline else "CANONICAL_ADDITION",
            "Canonical_Source": "LOOP3X full-universe authoritative materialization",
            "Canonical_Source_File": f"{SOURCE_URL}#FULL_UNIVERSE_SCREENING",
            "Canonical_Source_Version": SOURCE_VERSION,
            "Canonicalization_Batch": (
                "PubMed A/B/C baseline" if is_baseline else ("Batch05" if ordinal >= 1483 else "Batch02/03")
            ),
            "Provenance": (
                "Evidence Command Center 1,456 baseline; LOOP3X materialization"
                if is_baseline else addition.get("provenance", "")
            ),
            "Baseline_or_Addition": "BASELINE" if is_baseline else "ADDITION",
            "Addition_Number": "" if is_baseline else str(ordinal - 1456),
            "LOOP3X_Pass1": source_value(raw, indexes, "Pass1_Relevance"),
            "LOOP3X_Pass2": source_value(raw, indexes, "Pass2_Scientific_Fit"),
            "LOOP3X_Final_Class": source_value(raw, indexes, "Pass3_Final_Class"),
            "LOOP3X_Priority": source_value(raw, indexes, "Priority_Final"),
            "Domain": source_value(raw, indexes, "Domain_LOOP3X"),
            "Manuscript_Layer": source_value(raw, indexes, "Manuscript_Layer"),
            "Section": source_value(raw, indexes, "Section"),
            "Full_Text_Required": source_value(raw, indexes, "Full_Text_Required"),
            "Contradictory_Flag": source_value(raw, indexes, "Contradictory"),
            "Replace_Existing_Flag": source_value(raw, indexes, "Replace_Existing"),
            "Integrity_Status": source_value(raw, indexes, "Integrity_Status_LOOP"),
            "Freeze_Change_Candidate": source_value(raw, indexes, "Freeze_Change_Candidate"),
            "Overlap_Family": source_value(raw, indexes, "Overlap_Family"),
            "Human_Review_Status": source_value(raw, indexes, "Adjudication Status"),
            "Notes": source_value(raw, indexes, "LOOP_Notes"),
        })

    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / "MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv"
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(materialized)
    print(f"Wrote {len(materialized)} records to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
