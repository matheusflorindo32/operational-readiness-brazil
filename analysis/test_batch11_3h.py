import csv
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch11_3h"


def canonical_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class Batch113HTests(unittest.TestCase):
    def test_exact_artifact_set(self):
        expected = {
            "TARGET_JOURNAL_HUMAN_DECISION_FINAL.csv", "JOH_CURRENT_AUTHOR_GUIDELINES_REVALIDATION.csv",
            "JOH_EDITORIAL_REQUIREMENT_MAP.csv", "JOH_MANUSCRIPT_GAP_ANALYSIS.csv",
            "JOH_ARTICLE_TYPE_COMPATIBILITY_FINAL.md", "JOH_REPORTING_GUIDELINE_AUDIT.md",
            "JOH_AI_DISCLOSURE_POLICY_AUDIT.md", "JOH_APC_FINAL_VERIFICATION.md",
            "TARGET_JOURNAL_FREEZE.json", "BATCH11_3H_MANIFEST.json", "BATCH11_3H_REPORT.md",
        }
        self.assertEqual({p.name for p in OUT.iterdir() if p.is_file()}, expected)

    def test_human_target_and_freeze(self):
        with (OUT / "TARGET_JOURNAL_HUMAN_DECISION_FINAL.csv").open(encoding="utf-8", newline="") as stream:
            row = next(csv.DictReader(stream))
        self.assertEqual(row["Human_Reviewer"], "Matheus Florindo de Deus")
        self.assertEqual(row["Target_Journal"], "Journal of Occupational Health")
        self.assertEqual(row["Target_Article_Type"], "Review Article")
        self.assertEqual(row["Target_Status"], "HUMAN_SELECTED")
        self.assertTrue(all(row[field] == "0" for field in ["Scientific_Mutation", "Claim_Ready_Mutation", "CEF_Mutation", "Zotero_Mutation", "Brazil_Mutation", "Authorship_Mutation"]))

    def test_live_requirements_and_no_guideline_change(self):
        with (OUT / "JOH_CURRENT_AUTHOR_GUIDELINES_REVALIDATION.csv").open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertTrue(all(row["Live_Revalidation_Status"] == "VERIFIED" for row in rows))
        self.assertTrue(all(row["Author_Guideline_Change_Detected"] == "NO" for row in rows))
        requirements = {row["Guideline_Item"]: row["JOH_Current_Requirement"] for row in rows}
        self.assertEqual(requirements["Maximum manuscript word count"], "6000")
        self.assertEqual(requirements["References"], "No limit")
        self.assertEqual(requirements["Figures/tables"], "Maximum 6 combined")

    def test_manifest_and_source_freeze(self):
        manifest = json.loads((OUT / "BATCH11_3H_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["gate"], "TARGET_JOURNAL_HUMAN_SELECTION_PASS")
        self.assertEqual(manifest["freeze_gate"], "TARGET_JOURNAL_FREEZE_COMPLETE")
        self.assertEqual(manifest["next_gate"], "GO_JOH_EDITORIAL_ADAPTATION")
        self.assertEqual(manifest["qa"]["human_journal_selection"], "1/1")
        self.assertEqual(manifest["qa"]["official_guidelines_live_revalidated"], "YES")
        self.assertEqual(manifest["input_manuscript"]["docx_sha256"], "f5886dd8e715ee5d4666213b5b59027e382185a3ae19ce7959417ce6fe672030")
        self.assertEqual(manifest["input_manuscript"]["markdown_sha256_canonical_lf"], canonical_sha(ROOT / "batch11_2h" / "International_v1.3-FINAL-SCIENTIFIC-FREEZE.md"))
        self.assertEqual(manifest["qa"]["scientific_mutation"], 0)
        self.assertEqual(manifest["qa"]["cef_mutation"], 0)
        self.assertEqual(manifest["qa"]["zotero_mutation"], 0)

    def test_ai_and_reporting_guards(self):
        ai = (OUT / "JOH_AI_DISCLOSURE_POLICY_AUDIT.md").read_text(encoding="utf-8")
        reporting = (OUT / "JOH_REPORTING_GUIDELINE_AUDIT.md").read_text(encoding="utf-8")
        self.assertIn("HUMAN_INPUT_REQUIRED", ai)
        self.assertIn("PRISMA_CLAIM = NO", reporting)
        self.assertIn("RECORD_CLAIM = NO", reporting)


if __name__ == "__main__":
    unittest.main()
