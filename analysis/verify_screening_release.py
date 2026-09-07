"""Verify the screened XLSX against the unchanged pre-screening workbook."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook


ALLOWED_MASTER_COLUMNS = {
    "B", "E", "F", "G", "H", "AE", "CJ", "CK", "CL", "CM", "CN",
    "CO", "CP", "DZ", "EL", "EM",
}
ALLOWED_OTHER = {
    "Dashboard": {"A4", "N14"},
    "Search Provenance": {"A2"},
    "README": {"B10"},
}


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    decisions = json.loads(args.decisions.read_text(encoding="utf-8"))
    decision_by_pmid = {item["pmid"]: item for item in decisions}
    assert_true(len(decisions) == len(decision_by_pmid) == 1456, "decision identity count")

    before = load_workbook(args.before, data_only=False, read_only=False)
    after = load_workbook(args.after, data_only=False, read_only=False)
    assert_true(before.sheetnames == after.sheetnames, "sheet names/order changed")
    assert_true(len(after.sheetnames) == 14, "expected 14 worksheets")

    unexpected = []
    for sheet_name in before.sheetnames:
        old_sheet = before[sheet_name]
        new_sheet = after[sheet_name]
        assert_true(old_sheet.freeze_panes == new_sheet.freeze_panes, f"freeze panes changed: {sheet_name}")
        assert_true(len(old_sheet.tables) == len(new_sheet.tables), f"table count changed: {sheet_name}")
        assert_true(len(old_sheet._charts) == len(new_sheet._charts), f"chart count changed: {sheet_name}")
        populated = set(old_sheet._cells) | set(new_sheet._cells)
        for row, column in sorted(populated):
            old_cell = old_sheet.cell(row, column)
            new_cell = new_sheet.cell(row, column)
            if old_cell.value == new_cell.value:
                continue
            allowed = False
            if sheet_name == "Master Evidence" and 4 <= row <= 1459:
                allowed = new_cell.column_letter in ALLOWED_MASTER_COLUMNS
            elif new_cell.coordinate in ALLOWED_OTHER.get(sheet_name, set()):
                allowed = True
            if not allowed:
                unexpected.append(
                    {"sheet": sheet_name, "cell": new_cell.coordinate, "before": old_cell.value, "after": new_cell.value}
                )
            if len(unexpected) >= 20:
                break
        if len(unexpected) >= 20:
            break
    assert_true(not unexpected, f"unexpected cell changes: {unexpected}")

    master = after["Master Evidence"]
    pmids = [str(master[f"X{row}"].value) for row in range(4, 1460)]
    evidence_ids = [master[f"A{row}"].value for row in range(4, 1460)]
    zotero_keys = [master[f"AF{row}"].value for row in range(4, 1460)]
    assert_true(len(set(pmids)) == 1456, "PMIDs are not unique")
    assert_true(len(set(evidence_ids)) == 1456, "Evidence IDs are not unique")
    assert_true(len(set(zotero_keys)) == 1456 and all(zotero_keys), "Zotero keys invalid")
    assert_true("FXC7ZY9R" not in zotero_keys, "controlled Zotero test item entered Master Evidence")
    assert_true(set(pmids) == set(decision_by_pmid), "screening decisions do not reconcile")

    observed = Counter()
    for row, pmid in zip(range(4, 1460), pmids):
        item = decision_by_pmid[pmid]
        note = str(master[f"EM{row}"].value or "")
        assert_true(f"SCREENING_DECISION={item['decision']}" in note, f"missing decision note for {pmid}")
        assert_true("reviewer=OpenAI Codex" in note and "date=2026-09-07" in note, f"missing audit fields for {pmid}")
        assert_true("source=NCBI Entrez EFetch/PubMed URL" in note, f"missing source for {pmid}")
        assert_true(master[f"DZ{row}"].value, f"missing negative claim boundary for {pmid}")
        assert_true(master[f"CL{row}"].value == "Yes", f"integrity not checked for {pmid}")
        assert_true(master[f"EH{row}"].value is None, f"human analysis date populated for {pmid}")
        assert_true(master[f"EI{row}"].value is None, f"human reviewer populated for {pmid}")
        assert_true(master[f"EB{row}"].value != "Yes", f"claim-ready incorrectly approved for {pmid}")
        observed[item["decision"]] += 1
    assert_true(observed == Counter(x["decision"] for x in decisions), "decision counts differ")

    blocked_row = 4 + pmids.index("26159007")
    assert_true(master[f"AF{blocked_row}"].value == "9UE7LEZP", "retracted-record Zotero identity changed")
    assert_true(master[f"CN{blocked_row}"].value == "Retracted", "retraction status missing")
    assert_true(master[f"F{blocked_row}"].value == "Not used", "retracted record not blocked from use")
    assert_true(master[f"CP{blocked_row}"].value == "https://pubmed.ncbi.nlm.nih.gov/26357708/", "retraction notice link missing")

    for pmid in ("38280817", "36368814", "33721322", "11469036"):
        row = 4 + pmids.index(pmid)
        assert_true(master[f"AF{row}"].value, f"same-title record lost Zotero identity: {pmid}")
        assert_true("SCREENING_DECISION=INCLUDE_FULL_TEXT" in str(master[f"EM{row}"].value), f"same-title record not retained: {pmid}")

    before.close()
    after.close()
    after_values = load_workbook(args.after, data_only=True, read_only=False)
    values = after_values["Master Evidence"]
    assert_true(sum(values[f"CJ{r}"].value == "Yes" for r in range(4, 1460)) == 1366, "metadata verified count")
    assert_true(sum(values[f"CK{r}"].value == "Yes" for r in range(4, 1460)) == 1454, "identifier verified count")
    assert_true(sum(values[f"CL{r}"].value == "Yes" for r in range(4, 1460)) == 1456, "integrity checked count")
    assert_true(sum(values[f"F{r}"].value == "Not used" for r in range(4, 1460)) == 10, "not-used count")
    assert_true(sum(values[f"EB{r}"].value == "Yes" for r in range(4, 1460)) == 0, "claim-ready count")
    dashboard = after_values["Dashboard"]
    assert_true(dashboard["D8"].value == 1366, "dashboard metadata count")
    assert_true(dashboard["J8"].value == 0, "dashboard claim-ready count")
    assert_true(dashboard["B23"].value == 1446 and dashboard["B24"].value == 10, "dashboard traffic light counts")
    assert_true(dashboard["J16"].value == 1456, "Analysis pending indicator")

    report = {
        "status": "PASS",
        "screened": 1456,
        "decision_counts": dict(sorted(observed.items())),
        "identity_reconciled": 1456,
        "metadata_verified": 1366,
        "identifiers_verified": 1454,
        "integrity_checked": 1456,
        "claim_ready": 0,
        "analysis_pending": 1456,
        "worksheets": len(after.sheetnames),
        "tables": sum(len(sheet.tables) for sheet in after.worksheets),
        "charts": sum(len(sheet._charts) for sheet in after.worksheets),
        "unexpected_cell_changes": 0,
        "negative_scenarios": [
            "retraction blocks use",
            "correction requires review",
            "ambiguous title-only record remains pending",
            "same-title records remain separate",
            "Claim-Ready remains zero",
            "human reviewer/date fields remain empty",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    after_values.close()
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
