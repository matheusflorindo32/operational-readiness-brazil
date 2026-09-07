"""Regression contract for preserved pre-analysis gates and current screening."""

import csv
import json
import unittest
import xml.etree.ElementTree as ET
import zipfile

from audit_pubmed_structure import NS, ROOT, WORKBOOK, workbook_cells


class PreanalysisContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sheets = workbook_cells(WORKBOOK)
        cls.master = cls.sheets["Master Evidence"]
        cls.report = ROOT / "reporting/preanalysis/2026-09-06"

    def test_all_identity_triplets_preserved(self):
        with (self.report / "evidence-identity-map.csv").open(encoding="utf-8") as f:
            expected = list(csv.DictReader(f))
        actual = [
            {
                "evidence_id": self.master[f"A{r}"],
                "pmid": self.master[f"X{r}"],
                "zotero_key": self.master[f"AF{r}"],
            }
            for r in range(4, 1460)
        ]
        self.assertEqual(actual, expected)
        self.assertEqual(len({r["evidence_id"] for r in actual}), 1456)
        self.assertNotIn("FXC7ZY9R", {r["zotero_key"] for r in actual})

    def test_current_native_sheets_and_xlsx_counts_agree(self):
        live = json.loads(
            (ROOT / "reporting/screening/2026-09-07/drive-sync-validation.json").read_text(
                encoding="utf-8"
            )
        )
        notes = [self.master[f"EM{row}"] for row in range(4, 1460)]
        for decision, expected in live["decision_counts"].items():
            self.assertEqual(
                sum(f"SCREENING_DECISION={decision}" in note for note in notes), expected
            )
        self.assertEqual(live["rows"], 1456)
        self.assertEqual(live["unique_pmids"], 1456)
        self.assertEqual(live["unique_zotero_keys"], 1456)
        self.assertFalse(live["controlled_key_present"])
        self.assertEqual(live["claim_ready"], 0)
        self.assertEqual(live["human_fields_populated"], 0)
        self.assertEqual(live["negative_claim_boundaries"], 1456)
        self.assertTrue(live["disposable_copy_tested_and_deleted"])

    def test_no_scientific_approval_and_visible_imported_signal(self):
        self.assertEqual(sum(self.master[f"EB{r}"] == "Yes" for r in range(4, 1460)), 0)
        self.assertEqual(str(self.sheets["Dashboard"]["J16"]), "1456")
        self.assertEqual(str(self.sheets["Dashboard"]["B24"]), "10")
        self.assertEqual(str(self.sheets["Dashboard"]["B23"]), "1446")
        self.assertEqual(self.master["X1174"], "26159007")
        self.assertIn("Retracted Publication", self.master["Q1174"])
        self.assertIn("🔴", self.master["C1174"])
        self.assertEqual(self.master["CJ1174"], "Yes")
        self.assertEqual(self.master["CL1174"], "Yes")
        self.assertEqual(self.master["CN1174"], "Retracted")
        self.assertIn("SCREENING_DECISION=BLOCKED_INTEGRITY", self.master["EM1174"])

    def test_both_engines_pass_same_synthetic_scenarios(self):
        xlsx = json.loads(
            (self.report / "xlsx-functional-tests.json").read_text(encoding="utf-8")
        )
        native = json.loads(
            (self.report / "sheets-functional-tests.json").read_text(encoding="utf-8")
        )["cases"]
        self.assertEqual(len(xlsx), 24)
        self.assertEqual(len(native), 24)
        for a, b in zip(xlsx, native):
            self.assertTrue(a["pass"] and b["pass"])
            for key in ("name", "ready", "reason", "light"):
                self.assertEqual(a[key], b[key])

    def test_stable_ids_are_values_and_headers_frozen(self):
        with zipfile.ZipFile(WORKBOOK) as z:
            master = ET.fromstring(z.read("xl/worksheets/sheet3.xml"))
            cells = {
                c.attrib["r"]: c for c in master.findall(".//m:sheetData/m:row/m:c", NS)
            }
            for row in range(4, 1460):
                self.assertIsNone(cells[f"A{row}"].find("m:f", NS))
            self.assertEqual(master.find(".//m:pane", NS).attrib["ySplit"], "3")


if __name__ == "__main__":
    unittest.main()
