import copy
import json
import unittest
from pathlib import Path

from gate2_import_guard import evaluate_import_gate, validate_row


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "reporting" / "adjudication" / "2026-09-15" / "first-cycle-high-rigor.json"


class Gate2HighRigorControlsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.rows = cls.data["dossiers"]

    def test_g2_001_recommendation_does_not_populate_human_decision(self) -> None:
        self.assertTrue(all(row["decisao_humana"] == "" for row in self.rows))

    def test_g2_002_reviewer_required(self) -> None:
        row = copy.deepcopy(self.rows[0]); row["decisao_humana"] = "Confirmar bloqueio"
        self.assertIn("incomplete_human_adjudication", validate_row(row))

    def test_g2_003_date_required(self) -> None:
        row = self._complete(); row["data_humana"] = ""
        self.assertIn("incomplete_human_adjudication", validate_row(row))

    def test_g2_004_justification_required(self) -> None:
        row = self._complete(); row["justificativa_humana"] = ""
        self.assertIn("incomplete_human_adjudication", validate_row(row))

    def test_g2_005_claim_ready_remains_false(self) -> None:
        self.assertTrue(all(row["claim_ready"] == "BLOQUEADO" for row in self.rows))

    def test_g2_006_zotero_unchanged(self) -> None:
        self.assertTrue(self.data["controls"]["zotero_unchanged"])

    def test_g2_007_master_evidence_unchanged(self) -> None:
        self.assertEqual(
            self.data["controls"]["master_sha256_before"],
            self.data["controls"]["master_sha256_after"],
        )

    def test_g2_008_unsupported_dropdown_rejected(self) -> None:
        row = self._complete(); row["decisao_humana"] = "Aprovar automaticamente"
        self.assertIn("unsupported_human_decision", validate_row(row))

    def test_g2_009_pmid_unique(self) -> None:
        self.assertEqual(len({row["pmid"] for row in self.rows}), len(self.rows))

    def test_g2_010_zotero_key_unique(self) -> None:
        self.assertEqual(len({row["zotero_key"] for row in self.rows}), len(self.rows))

    def test_g2_011_retraction_relation_preserved(self) -> None:
        critical = next(row for row in self.rows if row["pmid"] == "26159007")
        self.assertEqual(critical["relacao_editorial"], "RetractionIn")
        self.assertNotIn("retraction_relation_not_preserved", validate_row(critical))

    def test_g2_012_missing_doi_explicit(self) -> None:
        missing = [row for row in self.rows if not row["doi"]]
        self.assertTrue(missing)
        self.assertTrue(all(row["doi_status"] == "NOT FOUND IN AUDITED SOURCE" for row in missing))

    def test_g2_013_missing_notice_pmid_explicit(self) -> None:
        row = next(row for row in self.rows if row["pmid"] == "15460628")
        self.assertEqual(row["editorial_notice_pmid_status"], "NOT FOUND")

    def test_g2_014_conflict_blocks_import(self) -> None:
        row = self._complete(); row["human_conflict"] = True
        self.assertIn("human_conflict_requires_resolution", validate_row(row))

    def test_g2_015_dry_run_required(self) -> None:
        result = evaluate_import_gate(
            [self._complete()], dry_run_present=False,
            zotero_unchanged=True, master_evidence_unchanged=True,
        )
        self.assertFalse(result["ready"])
        self.assertIn("dry_run_required", result["reasons"])

    def _complete(self):
        row = copy.deepcopy(self.rows[1])
        row.update({
            "revisor_humano": "Revisor identificado",
            "data_humana": "2026-09-15",
            "decisao_humana": "Investigar relação editorial",
            "justificativa_humana": "Justificativa documentada pelo revisor.",
            "human_decision_provenance": "human_entered",
        })
        return row


if __name__ == "__main__":
    unittest.main()
