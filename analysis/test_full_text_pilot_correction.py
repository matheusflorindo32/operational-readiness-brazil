import csv
import json
import unittest
from pathlib import Path

from analysis.build_full_text_pilot_correction import ORIGINAL, OUTPUT, build, sha256


class FullTextPilotCorrectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = build()
        with (OUTPUT / "corrected-records.csv").open(encoding="utf-8-sig", newline="") as handle:
            cls.records = {row["evidence_id"]: row for row in csv.DictReader(handle)}
        with (OUTPUT / "corrected-appraisal-domain-ledger.csv").open(encoding="utf-8-sig", newline="") as handle:
            cls.appraisal = list(csv.DictReader(handle))

    def rows(self, evidence_id):
        return [row for row in self.appraisal if row["evidence_id"] == evidence_id]

    def test_01_mixed_methods_not_complete_with_only_5x(self):
        for eid in ("EV-0787", "EV-0593"):
            codes = {row["criterion_code"] for row in self.rows(eid)}
            self.assertEqual(len(codes), 17)
            self.assertTrue({"S1", "S2", "1.1", "1.2", "1.3", "1.4", "1.5", "4.1", "4.2", "4.3", "4.4", "4.5", "5.1", "5.2", "5.3", "5.4", "5.5"}.issubset(codes))

    def test_02_mixed_qualitative_and_quantitative_components_are_appraised(self):
        for eid in ("EV-0787", "EV-0593"):
            components = {row["component"] for row in self.rows(eid)}
            self.assertIn("QUALITATIVE_COMPONENT", components)
            self.assertIn("QUANTITATIVE_DESCRIPTIVE_COMPONENT", components)

    def test_03_instruments_match_evidence_class(self):
        expected = {
            "EV-0668": "SANRA", "EV-0787": "MMAT", "EV-0593": "MMAT",
            "EV-0758": "JBI Textual Evidence: Expert Opinion",
            "EV-0523": "JBI Textual Evidence: Expert Opinion",
        }
        for eid, tool in expected.items():
            self.assertEqual({row["tool"] for row in self.rows(eid)}, {tool})

    def test_04_every_instrument_has_a_version(self):
        self.assertTrue(all(row["tool_version"].strip() for row in self.appraisal))
        self.assertTrue(all(row["appraisal_tool_version"].strip() for row in self.records.values()))

    def test_05_legacy_jbi_text_and_opinion_is_absent(self):
        self.assertNotIn("JBI Text and Opinion", {row["tool"] for row in self.appraisal})
        for eid in ("EV-0758", "EV-0523"):
            self.assertEqual(self.records[eid]["appraisal_tool"], "JBI Textual Evidence: Expert Opinion")

    def test_06_sanra_is_not_a_risk_of_bias_appraisal(self):
        row = self.records["EV-0668"]
        self.assertEqual(row["appraisal_type"], "METHODOLOGICAL_QUALITY_APPRAISAL")
        self.assertEqual(row["methodological_quality_appraisal"], "YES")
        self.assertEqual(row["risk_of_bias_appraisal"], "NO")

    def test_07_commentary_is_not_empirical(self):
        row = self.records["EV-0523"]
        self.assertEqual(row["evidence_class"], "COMMENTARY_EXPERT_OPINION")
        self.assertEqual(row["original_data"], "NO")
        self.assertEqual(row["empirical_effect_estimate"], "NO")
        self.assertEqual(row["eligibility_contextual_source"], "HUMAN_DECISION_REQUIRED")

    def test_08_aam_identity_is_retained(self):
        self.assertEqual(self.records["EV-0787"]["version_status"], "AUTHOR_ACCEPTED_MANUSCRIPT")
        self.assertEqual(self.records["EV-0425"]["version_status"], "AUTHOR_ACCEPTED_MANUSCRIPT")
        self.assertEqual(self.records["EV-0425"]["extraction_version"], "AAM_USED_FOR_EXTRACTION")
        self.assertEqual(self.records["EV-0425"]["vor_comparison_status"], "VERSION_OF_RECORD_COMPARISON_PENDING")

    def test_09_human_confirmation_remains_empty(self):
        human_fields = ("human_reviewer", "human_review_date", "human_decision", "human_justification", "human_confirmation", "human_appraisal_confirmed")
        for row in self.records.values():
            self.assertTrue(all(row[field] == "" for field in human_fields))
        self.assertTrue(all(row["human_confirmed"] == "" for row in self.appraisal))

    def test_10_claim_ready_remains_fail_closed(self):
        self.assertTrue(all(row["claim_ready"] == "NO" for row in self.records.values()))
        self.assertEqual(self.summary["claim_ready"], 0)

    def test_11_retraction_quarantine_is_unchanged(self):
        quarantine = Path("reporting/nonblocking/2026-09-16/integrity-quarantine.csv").read_text(encoding="utf-8-sig")
        self.assertIn("26159007", quarantine)
        self.assertIn("BLOCKED_INTEGRITY", quarantine)
        self.assertIn("NOT USED", quarantine)
        self.assertNotIn("26159007", {row["pmid"] for row in self.records.values()})

    def test_12_control_item_is_outside_scientific_queues(self):
        self.assertNotIn("FXC7ZY9R", {row["zotero_key"] for row in self.records.values()})

    def test_original_pilot_is_preserved_by_hash(self):
        preservation = json.loads((OUTPUT / "source-preservation.json").read_text(encoding="utf-8"))
        for name, meta in preservation["files"].items():
            self.assertEqual(sha256(ORIGINAL / name), meta["sha256"])

    def test_red_team_is_complete_for_all_records(self):
        with (OUTPUT / "methodological-red-team-ledger.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 10)
        self.assertTrue(all(row["overall"] == "PASS" for row in rows))
        self.assertTrue(all(row["exact_claim_location_required"] == "PASS" for row in rows))


if __name__ == "__main__":
    unittest.main()
