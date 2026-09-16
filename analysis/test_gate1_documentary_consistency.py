import json
import unittest
from pathlib import Path

from audit_pubmed_structure import workbook_cells


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "outputs" / "8a39e3c813da" / "PREMIUM_ELITE_DIAMANTE_Evidence_Command_Center.xlsx"


class Gate1DocumentaryConsistencyTest(unittest.TestCase):
    def test_local_dashboard_has_canonical_traffic_light(self) -> None:
        sheets = workbook_cells(WORKBOOK)
        dashboard = sheets["Dashboard"]
        self.assertEqual(str(dashboard["B22"]), "0")
        self.assertEqual(str(dashboard["B23"]), "1446")
        self.assertEqual(str(dashboard["B24"]), "10")

    def test_current_documents_do_not_publish_stale_count(self) -> None:
        paths = [
            ROOT / "README.md",
            ROOT / "CHANGELOG.md",
            ROOT / "reporting" / "CHECKLIST.md",
            ROOT / "docs" / "PUBMED_PREANALYSIS_GATE_2026-09-06.md",
            ROOT / "docs" / "PUBMED_TITLE_ABSTRACT_SCREENING_2026-09-07.md",
        ]
        stale = "1 vermelho, 1.455 amarelos"
        for path in paths:
            self.assertNotIn(stale, path.read_text(encoding="utf-8"), path)

    def test_drive_validation_preserves_identity_and_decisions(self) -> None:
        path = ROOT / "reporting" / "screening" / "2026-09-07" / "drive-sync-validation.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "PASS")
        self.assertEqual(data["rows"], 1456)
        self.assertEqual(data["unique_pmids"], 1456)
        self.assertEqual(data["unique_zotero_keys"], 1456)
        self.assertFalse(data["controlled_key_present"])
        self.assertEqual(data["not_used"], 10)
        self.assertEqual(data["claim_ready"], 0)
        self.assertEqual(data["human_fields_populated"], 0)


if __name__ == "__main__":
    unittest.main()
