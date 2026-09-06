"""Regression contract for the published, unscreened production workbook."""

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

    def test_native_sheets_and_xlsx_agree_for_every_gate_row(self):
        live = json.loads(
            (self.report / "canonical-reconciliation.json").read_text(encoding="utf-8")
        )
        for column, values in live["gate_values"].items():
            for row, value in enumerate(values, 4):
                self.assertEqual(self.master[f"{column}{row}"], value, f"{column}{row}")
        self.assertTrue(live["permissions_preserved"])
        self.assertTrue(live["sort_insert_identity"])

    def test_no_scientific_approval_and_visible_imported_signal(self):
        self.assertEqual(sum(self.master[f"EB{r}"] == "Yes" for r in range(4, 1460)), 0)
        self.assertEqual(str(self.sheets["Dashboard"]["J16"]), "1456")
        self.assertEqual(str(self.sheets["Dashboard"]["B24"]), "1")
        self.assertEqual(str(self.sheets["Dashboard"]["B23"]), "1455")
        self.assertEqual(self.master["X1174"], "26159007")
        self.assertIn("Retracted Publication", self.master["Q1174"])
        self.assertIn("🔴", self.master["C1174"])
        self.assertNotEqual(self.master["CJ1174"], "Yes")

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
