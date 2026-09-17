import csv
import json
import tempfile
import unittest
from pathlib import Path

from analysis.build_nonblocking_queues import ROOT, build


class NonBlockingQueuesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = ROOT / "reporting/nonblocking/2026-09-16"
        cls.summary = json.loads((cls.output / "run-summary.json").read_text(encoding="utf-8"))

    def rows(self, name):
        with (self.output / name).open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_partition_counts_and_no_claim_release(self):
        self.assertEqual(self.summary["full_text_candidates"], 1206)
        self.assertEqual(self.summary["pending_adjudication"], 240)
        self.assertEqual(self.summary["quarantined_retraction"], 1)
        for name in ("integrity-quarantine.csv", "editorial-review-queue.csv", "full-text-priority-queue.csv", "pending-adjudication-queue.csv"):
            self.assertTrue(all(row["claim_ready"] == "NO" for row in self.rows(name)))

    def test_human_fields_remain_blank(self):
        for name in ("integrity-quarantine.csv", "editorial-review-queue.csv", "pending-adjudication-queue.csv"):
            for row in self.rows(name):
                self.assertEqual(row.get("human_reviewer", ""), "")
                self.assertEqual(row.get("human_date", ""), "")
                self.assertEqual(row.get("human_decision", ""), "")

    def test_control_item_is_absent_and_resolution_scope_is_complete(self):
        for path in self.output.glob("*.csv"):
            self.assertNotIn("FXC7ZY9R", path.read_text(encoding="utf-8-sig"))
        self.assertEqual(len(self.rows("metadata-resolution-ledger.csv")), 90)
        self.assertEqual(len(self.rows("doi-resolution-ledger.csv")), 2)
        self.assertEqual(len(self.rows("editorial-review-queue.csv")), 18)

    def test_manifest_covers_outputs_without_self_reference(self):
        manifest = json.loads((self.output / "manifest.json").read_text(encoding="utf-8"))
        self.assertNotIn("manifest.json", manifest)
        self.assertEqual(set(manifest), {p.name for p in self.output.iterdir() if p.is_file() and p.name != "manifest.json"})

    def test_generator_reproduces_committed_summary_when_audited_raw_data_exist(self):
        external = Path(r"C:\Users\mathe\Documents\Codex\2026-08-26\zotero-plugin-zotero-openai-curated-remote\outputs\zotero-backups\2026-09-16-nonblocking\audit-full")
        if not external.exists():
            self.skipTest("Audited raw PubMed backup is intentionally external to Git")
        with tempfile.TemporaryDirectory() as temp:
            rebuilt = build(external / "pubmed-current-records.json", external / "screening-decisions.json", Path(temp))
        # ``generated_on`` records the execution date and is expected to change
        # when the deterministic rebuild is audited on a later day.  Compare
        # every scientific and operational field while keeping the timestamp
        # outside the reproducibility assertion.
        rebuilt_without_date = {key: value for key, value in rebuilt.items() if key != "generated_on"}
        summary_without_date = {key: value for key, value in self.summary.items() if key != "generated_on"}
        self.assertEqual(rebuilt_without_date, summary_without_date)


if __name__ == "__main__":
    unittest.main()
