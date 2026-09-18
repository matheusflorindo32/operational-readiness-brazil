from __future__ import annotations

import csv
import hashlib
import json
import unittest
import zipfile
from pathlib import Path

try:
    from audit_xlsx_identity import semantic_sha256
except ModuleNotFoundError:
    from analysis.audit_xlsx_identity import semantic_sha256


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reporting/full-text/2026-09-17/pilot-02"
WORKBOOK = ROOT / "outputs/full-text/2026-09-17/Operational_Readiness_Full_Text_Pilot_02.xlsx"


def rows(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class FullTextPilot02Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = rows("pilot-records.csv")
        cls.appraisal = rows("appraisal-domain-ledger.csv")
        cls.red = rows("red-team-ledger.csv")
        cls.human = rows("human-review-queue-pilots-01-02.csv")
        cls.selection = rows("selection-audit.csv")
        cls.versions = rows("version-ledger.csv")
        cls.summary = json.loads((OUT / "run-summary.json").read_text(encoding="utf-8"))

    def test_01_deterministic_selection_and_no_pilot01_reuse(self) -> None:
        self.assertEqual([r["evidence_id"] for r in self.selection], ["EV-0367","EV-0176","EV-0171","EV-0160","EV-0157","EV-0091","EV-1328","EV-0896","EV-0791","EV-0723"])
        pilot1 = {r["evidence_id"] for r in rows("../pilot-01-methodological-correction/corrected-records.csv")}
        self.assertFalse(pilot1 & {r["evidence_id"] for r in self.records})

    def test_02_identity_and_full_text_complete(self) -> None:
        self.assertEqual(len(self.records), 10)
        self.assertTrue(all(r["full_text_obtained"] == "YES" and r["identity_status"] == "MATCH_CONFIRMED" for r in self.records))
        self.assertEqual(len({r["pmid"] for r in self.records}), 10)
        self.assertEqual(len({r["pmcid"] for r in self.records}), 10)

    def test_03_control_and_retracted_record_are_excluded(self) -> None:
        self.assertNotIn("FXC7ZY9R", {r["zotero_key"] for r in self.records})
        self.assertNotIn("26159007", {r["pmid"] for r in self.records})

    def test_04_all_human_fields_blank_and_claims_closed(self) -> None:
        fields = ["human_reviewer","human_review_date","human_decision","human_justification","human_confirmation"]
        self.assertTrue(all(not r[f] for r in self.records for f in fields))
        self.assertTrue(all(r["claim_ready"] == "NO" and r["record_status"] == "HUMAN_REVIEW_REQUIRED" for r in self.records))

    def test_05_tool_matches_evidence_class(self) -> None:
        mapping = {"QUALITATIVE_EVIDENCE":"JBI Qualitative Research", "MIXED_METHODS_EVIDENCE":"MMAT", "QUANTITATIVE_EVIDENCE":"JBI Quasi-Experimental Studies"}
        self.assertTrue(all(r["appraisal_tool"] == mapping[r["evidence_class"]] for r in self.records))

    def test_06_mixed_methods_are_full_mmat(self) -> None:
        for evidence_id in ("EV-0171", "EV-0160"):
            current = [r for r in self.appraisal if r["evidence_id"] == evidence_id]
            self.assertEqual(len(current), 17)
            self.assertEqual({r["criterion_code"] for r in current}, {"S1","S2",*[f"1.{i}" for i in range(1,6)],*[f"4.{i}" for i in range(1,6)],*[f"5.{i}" for i in range(1,6)]})

    def test_07_qualitative_and_quasi_appraisals_complete(self) -> None:
        for evidence_id in ("EV-0367","EV-0176","EV-0157","EV-0723"):
            self.assertEqual(len([r for r in self.appraisal if r["evidence_id"] == evidence_id]), 10)
        for evidence_id in ("EV-0091","EV-1328","EV-0896","EV-0791"):
            self.assertEqual(len([r for r in self.appraisal if r["evidence_id"] == evidence_id]), 9)

    def test_08_no_global_score_and_appraisal_is_provisional(self) -> None:
        self.assertTrue(all(r["global_quality_score"] == "NOT_CALCULATED" for r in self.records))
        self.assertTrue(all(not r["human_confirmed"] and r["judgment_ai_provisional"] for r in self.appraisal))

    def test_09_aam_versions_are_explicit(self) -> None:
        aams = [r for r in self.versions if r["source_version"] == "AUTHOR_ACCEPTED_MANUSCRIPT"]
        self.assertEqual({r["evidence_id"] for r in aams}, {"EV-0367","EV-1328","EV-0791"})
        self.assertTrue(all(r["vor_comparison"] != "NOT_APPLICABLE" for r in aams))

    def test_10_red_team_all_checks_pass(self) -> None:
        check_fields = [f for f in self.red[0] if f not in {"evidence_id","pmid","record_gate","finding","overall"}]
        self.assertEqual(len(check_fields), 16)
        self.assertTrue(all(r["overall"] == "PASS" and all(r[f] == "PASS" for f in check_fields) for r in self.red))

    def test_11_human_queue_combines_both_pilots_without_decisions(self) -> None:
        self.assertEqual(len(self.human), 20)
        self.assertEqual({r["pilot"] for r in self.human}, {"PILOT_01_CORRECTED", "PILOT_02"})
        self.assertTrue(all(not r[f] for r in self.human for f in ["human_reviewer","human_review_date","human_decision","human_justification","human_confirmation"]))
        self.assertTrue(all(r["claim_ready"] == "NO" for r in self.human))

    def test_12_summary_preserves_fail_closed_gate(self) -> None:
        self.assertEqual(self.summary["decision"], "GO_PILOT_03")
        self.assertEqual(self.summary["human_decisions"], 0)
        self.assertEqual(self.summary["claim_ready"], 0)
        self.assertEqual(self.summary["scientific_pass"], "PROHIBITED")
        self.assertFalse(self.summary["zotero_modified"] or self.summary["master_evidence_modified"])

    def test_13_master_and_pilot01_preserved(self) -> None:
        preservation = json.loads((OUT / "source-preservation.json").read_text(encoding="utf-8"))
        master = ROOT / preservation["master_evidence"]["path"]
        self.assertEqual(hashlib.sha256(master.read_bytes()).hexdigest(), preservation["master_evidence"]["sha256"])
        pilot1 = ROOT / preservation["pilot_01_corrected"]["path"] / "corrected-records.csv"
        self.assertEqual(hashlib.sha256(pilot1.read_bytes()).hexdigest(), preservation["pilot_01_corrected"]["records_sha256"])

    def test_14_manifest_covers_delivered_ledgers(self) -> None:
        manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
        for name, metadata in manifest.items():
            target = OUT / name
            self.assertTrue(target.exists())
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), metadata["sha256"])

    def test_15_workbook_integrity_and_eight_sheets(self) -> None:
        self.assertTrue(WORKBOOK.exists())
        with zipfile.ZipFile(WORKBOOK) as archive:
            self.assertIsNone(archive.testzip())
            workbook_xml = archive.read("xl/workbook.xml").decode("utf-8")
            for name in ["Resumo","Seleção","Registros","Appraisal","Versões","Red Team","Proveniência","Revisão humana"]:
                self.assertIn(f'name="{name}"', workbook_xml)
        artifact = json.loads((OUT / "workbook-artifact.json").read_text(encoding="utf-8"))
        self.assertEqual(hashlib.sha256(WORKBOOK.read_bytes()).hexdigest(), artifact["binary_sha256"])
        self.assertEqual(semantic_sha256(WORKBOOK), artifact["semantic_sha256"])


if __name__ == "__main__":
    unittest.main()
