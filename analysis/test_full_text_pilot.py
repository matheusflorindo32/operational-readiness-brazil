import csv
import json
import tempfile
import unittest
from pathlib import Path

from analysis.build_full_text_pilot import DEFAULT_OUTPUT, build, claim_ready_allowed


class FullTextPilotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = DEFAULT_OUTPUT
        cls.summary = json.loads((cls.output / "run-summary.json").read_text(encoding="utf-8"))
        with (cls.output / "pilot-records.csv").open(encoding="utf-8-sig", newline="") as handle:
            cls.records = list(csv.DictReader(handle))

    @staticmethod
    def eligible_row():
        return {
            "full_text_obtained": "YES", "identity_status": "MATCH_CONFIRMED",
            "ai_full_text_decision": "INCLUDE_FULL_TEXT", "extraction_complete": "YES",
            "appraisal_complete_ai": "YES", "integrity_status": "INTEGRITY_CLEAR",
            "exact_location_complete": "YES", "boundary_complete": "YES",
            "transferability_complete": "YES", "human_confirmation": "YES",
            "editorial_hold": "NO",
        }

    def test_pilot_is_complete_but_no_human_or_claim_decision_is_simulated(self):
        self.assertEqual(len(self.records), 10)
        self.assertEqual(self.summary["full_text_obtained"], 10)
        self.assertEqual(self.summary["identity_match_confirmed"], 10)
        self.assertEqual(self.summary["human_decisions"], 0)
        self.assertEqual(self.summary["claim_ready"], 0)
        for row in self.records:
            for field in ("human_reviewer", "human_review_date", "human_decision", "human_justification", "human_confirmation"):
                self.assertEqual(row[field], "")
            self.assertEqual(row["claim_ready"], "NO")

    def test_every_fail_closed_prerequisite_blocks_claim_ready(self):
        base = self.eligible_row()
        self.assertTrue(claim_ready_allowed(base))
        failures = {
            "full_text_obtained": "NO", "identity_status": "UNRESOLVED",
            "ai_full_text_decision": "HUMAN_REVIEW_REQUIRED", "extraction_complete": "NO",
            "appraisal_complete_ai": "NO", "integrity_status": "BLOCKED_INTEGRITY",
            "exact_location_complete": "NO", "boundary_complete": "NO",
            "transferability_complete": "NO", "human_confirmation": "",
            "editorial_hold": "YES",
        }
        for field, value in failures.items():
            row = dict(base); row[field] = value
            with self.subTest(field=field):
                self.assertFalse(claim_ready_allowed(row))

    def test_missing_full_text_fails_the_build(self):
        with (
            tempfile.TemporaryDirectory() as raw,
            tempfile.TemporaryDirectory() as output,
            self.assertRaises(FileNotFoundError),
        ):
            build(Path(raw), Path(output))

    def test_control_item_and_retracted_record_are_excluded(self):
        self.assertNotIn("FXC7ZY9R", {row["zotero_key"] for row in self.records})
        self.assertNotIn("26159007", {row["pmid"] for row in self.records})
        quarantine = (Path(__file__).resolve().parents[1] / "reporting/nonblocking/2026-09-16/integrity-quarantine.csv").read_text(encoding="utf-8-sig")
        self.assertIn("26159007", quarantine)
        self.assertIn("BLOCKED_INTEGRITY", quarantine)
        self.assertIn("NOT USED", quarantine)

    def test_appraisal_is_design_specific_and_provisional(self):
        with (self.output / "appraisal-domain-ledger.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        tools = {row["evidence_id"]: row["tool"] for row in rows}
        self.assertEqual(tools["EV-0668"], "SANRA")
        self.assertEqual(tools["EV-0787"], "MMAT 2018")
        self.assertEqual(tools["EV-0523"], "JBI Text and Opinion")
        self.assertEqual(tools["EV-0503"], "JBI Qualitative Research")
        self.assertTrue(all(row["human_confirmed"] == "" for row in rows))

    def test_provenance_and_manifest_cover_all_outputs(self):
        with (self.output / "provenance-ledger.csv").open(encoding="utf-8-sig", newline="") as handle:
            provenance = list(csv.DictReader(handle))
        self.assertEqual(len(provenance), 30)
        raw_rows = [row for row in provenance if row["stage"] in {"RAW_PUBMED", "FULL_TEXT"}]
        self.assertEqual(len(raw_rows), 20)
        self.assertTrue(all(len(row["sha256"]) == 64 for row in raw_rows))
        manifest = json.loads((self.output / "manifest.json").read_text(encoding="utf-8"))
        expected = {path.name for path in self.output.iterdir() if path.is_file() and path.name != "manifest.json"}
        self.assertEqual(set(manifest), expected)


if __name__ == "__main__":
    unittest.main()
