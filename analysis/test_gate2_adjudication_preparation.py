import csv
import json
import unittest
import zipfile
from pathlib import Path

from audit_pubmed_structure import workbook_cells


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "reporting" / "adjudication" / "2026-09-15"
XLSX = ROOT / "outputs" / "adjudication" / "2026-09-15" / "GATE_2_Fila_Adjudicacao_Humana_18_Registros.xlsx"


class Gate2AdjudicationPreparationTest(unittest.TestCase):
    def test_source_dataset_is_exact_and_has_no_human_decision(self) -> None:
        data = json.loads((DATA_DIR / "priority-adjudication-source.json").read_text(encoding="utf-8"))
        rows = data["records"]
        self.assertEqual(len(rows), 18)
        self.assertEqual(len({row["pmid"] for row in rows}), 18)
        self.assertEqual(len({row["zotero_key"] for row in rows}), 18)
        self.assertEqual(sum(row["relacao_editorial"].startswith("Retraction") for row in rows), 1)
        self.assertEqual(sum(not row["relacao_editorial"].startswith("Retraction") for row in rows), 17)
        self.assertNotIn("FXC7ZY9R", {row["zotero_key"] for row in rows})
        for row in rows:
            self.assertEqual(row["revisor_humano"], "")
            self.assertEqual(row["data_humana"], "")
            self.assertEqual(row["decisao_humana"], "")
            self.assertEqual(row["justificativa_humana"], "")
            self.assertNotEqual(str(row["claim_ready"]).casefold(), "yes")

    def test_csv_matches_source_identity(self) -> None:
        with (DATA_DIR / "priority-adjudication-queue.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 18)
        self.assertEqual(len({row["pmid"] for row in rows}), 18)
        self.assertEqual(len({row["zotero_key"] for row in rows}), 18)

    def test_xlsx_queue_preserves_blank_human_fields_and_blocks_claims(self) -> None:
        with zipfile.ZipFile(XLSX) as archive:
            self.assertIsNone(archive.testzip())
            validations = b"".join(
                archive.read(name)
                for name in archive.namelist()
                if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
            )
            self.assertIn(b"P6:P23", validations)
        queue = workbook_cells(XLSX)["Fila"]
        pmids = [queue[f"C{row}"] for row in range(6, 24)]
        zotero_keys = [queue[f"E{row}"] for row in range(6, 24)]
        relations = [queue[f"G{row}"] for row in range(6, 24)]
        self.assertEqual(len(set(pmids)), 18)
        self.assertEqual(len(set(zotero_keys)), 18)
        self.assertEqual(sum(value.startswith("Retraction") for value in relations), 1)
        for row in range(6, 24):
            self.assertEqual([queue.get(f"{column}{row}", "") for column in "NOPQ"], ["", "", "", ""])
            self.assertEqual(queue[f"R{row}"], "BLOQUEADO")

    def test_drive_validation_matches_gate_controls(self) -> None:
        data = json.loads((DATA_DIR / "drive-validation.json").read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "PASS")
        self.assertEqual(data["queue_rows"], 18)
        self.assertEqual(data["human_decision_populated"], 0)
        self.assertEqual(data["claim_ready_released"], 0)
        self.assertFalse(data["controlled_key_present"])
        self.assertEqual(data["canonical_traffic_light"], {"green": 0, "yellow": 1446, "red": 10})


if __name__ == "__main__":
    unittest.main()
