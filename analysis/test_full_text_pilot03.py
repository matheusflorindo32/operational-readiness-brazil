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

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"reporting/full-text/2026-09-17/pilot-03"
WORKBOOK=ROOT/"outputs/full-text/2026-09-17/Operational_Readiness_Full_Text_Pilot_03.xlsx"

def rows(name):
    with (OUT/name).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def lf(path): return Path(path).read_bytes().replace(b"\r\n",b"\n").replace(b"\r",b"\n")

class Pilot03Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=rows("pilot-records.csv"); cls.appraisal=rows("appraisal-domain-ledger.csv")
        cls.red=rows("red-team-ledger.csv"); cls.human=rows("human-review-queue-pilots-01-03.csv")
        cls.selection=rows("selection-audit.csv"); cls.versions=rows("versions-ledger.csv")
        cls.summary=json.loads((OUT/"run-summary.json").read_text(encoding="utf-8"))

    def test_01_selection_is_exact_and_deterministic(self):
        expected=["EV-0629","EV-0592","EV-0515","EV-0439","EV-0405","EV-0335","EV-0316","EV-0282","EV-0252","EV-0167"]
        self.assertEqual([r["evidence_id"] for r in self.selection],expected)
        self.assertTrue(all(r["selection_rule"]=="FIRST_10_P1_PMC_AVAILABLE_NOT_IN_PILOTS_01_02" for r in self.selection))

    def test_02_no_reuse_across_three_pilots(self):
        prior=set()
        for path in [ROOT/"reporting/full-text/2026-09-17/pilot-01-methodological-correction/corrected-records.csv",ROOT/"reporting/full-text/2026-09-17/pilot-02/pilot-records.csv"]:
            with path.open(encoding="utf-8-sig",newline="") as f: prior|={r["evidence_id"] for r in csv.DictReader(f)}
        self.assertFalse(prior & {r["evidence_id"] for r in self.records})

    def test_03_identity_and_full_text_complete(self):
        self.assertEqual(len(self.records),10)
        self.assertTrue(all(r["identity_status"]=="MATCH_CONFIRMED" and r["full_text_obtained"]=="YES" for r in self.records))
        for field in ("evidence_id","pmid","pmcid","doi","zotero_key"):
            self.assertEqual(len({r[field] for r in self.records}),10)

    def test_04_forbidden_records_excluded(self):
        self.assertNotIn("FXC7ZY9R",{r["zotero_key"] for r in self.records})
        self.assertNotIn("26159007",{r["pmid"] for r in self.records})

    def test_05_integrity_clear_but_bounded(self):
        self.assertTrue(all(r["integrity_status"]=="INTEGRITY_CLEAR" for r in self.records))
        self.assertTrue(all("absence is not absolute proof" in r["integrity_detail"] for r in self.records))

    def test_06_human_fields_blank_and_claims_closed(self):
        fields=["human_reviewer","human_review_date","human_decision","human_justification","human_confirmation"]
        self.assertTrue(all(not r[f] for r in self.records for f in fields))
        self.assertTrue(all(r["claim_ready"]=="NO" and r["record_status"]=="HUMAN_REVIEW_REQUIRED" for r in self.records))

    def test_07_appraisal_routes_match_design(self):
        expected={"EV-0629":"JBI Qualitative Research","EV-0592":"JBI Qualitative Research","EV-0515":"JBI Qualitative Research","EV-0439":"JBI Analytical Cross Sectional Studies","EV-0405":"Protocol Methods Completeness Check","EV-0335":"JBI Qualitative Research","EV-0316":"SANRA","EV-0282":"MMAT","EV-0252":"MMAT Quantitative Descriptive","EV-0167":"JBI Quasi-Experimental Studies"}
        self.assertEqual({r["evidence_id"]:r["appraisal_tool"] for r in self.records},expected)

    def test_08_full_mmat_and_descriptive_mmat(self):
        self.assertEqual(len([r for r in self.appraisal if r["evidence_id"]=="EV-0282"]),17)
        self.assertEqual(len([r for r in self.appraisal if r["evidence_id"]=="EV-0252"]),7)

    def test_09_other_appraisals_complete(self):
        counts={eid:len([r for r in self.appraisal if r["evidence_id"]==eid]) for eid in {r["evidence_id"] for r in self.records}}
        self.assertEqual(counts,{"EV-0629":10,"EV-0592":10,"EV-0515":10,"EV-0439":8,"EV-0405":8,"EV-0335":10,"EV-0316":6,"EV-0282":17,"EV-0252":7,"EV-0167":9})

    def test_10_no_global_score_and_provisional_only(self):
        self.assertTrue(all(r["global_quality_score"]=="NOT_CALCULATED" for r in self.records))
        self.assertTrue(all(r["judgment_ai_provisional"] and not r["human_confirmed"] for r in self.appraisal))

    def test_11_aam_and_vor_status_explicit(self):
        aams=[r for r in self.versions if r["source_version"]=="AUTHOR_ACCEPTED_MANUSCRIPT"]
        self.assertEqual({r["evidence_id"] for r in aams},{"EV-0316","EV-0252","EV-0167"})
        self.assertEqual([r["evidence_id"] for r in aams if r["vor_comparison"]=="VOR_COMPARISON_PENDING"],["EV-0252"])

    def test_12_red_team_minimum_20_and_pass(self):
        fields=[f for f in self.red[0] if f not in {"evidence_id","pmid","record_gate","finding","overall"}]
        self.assertGreaterEqual(len(fields),20)
        self.assertTrue(all(r["overall"]=="PASS" and all(r[f]=="PASS" for f in fields) for r in self.red))

    def test_13_human_queue_cumulative_and_blank(self):
        self.assertEqual(len(self.human),30)
        self.assertEqual({r["pilot"] for r in self.human},{"PILOT_01_CORRECTED","PILOT_02","PILOT_03"})
        fields=["human_reviewer","human_review_date","human_decision","human_justification","human_confirmation"]
        self.assertTrue(all(not r[f] for r in self.human for f in fields))
        self.assertTrue(all(r["claim_ready"]=="NO" for r in self.human))

    def test_14_source_preserved(self):
        p=json.loads((OUT/"source-preservation.json").read_text(encoding="utf-8")); master=ROOT/p["master_evidence"]["path"]
        current=hashlib.sha256(master.read_bytes()).hexdigest()
        self.assertEqual(current,p["master_evidence"]["sha256_before"]); self.assertEqual(current,p["master_evidence"]["sha256_after"])

    def test_15_derived_variance_is_not_mislabeled_equal(self):
        d=json.loads((OUT/"pilot02-derived-variance.json").read_text(encoding="utf-8"))
        self.assertEqual(d["status"],"DOCUMENTED_DERIVED_FUNCTIONAL_VARIANCE")
        self.assertFalse(d["strict_semantic_equal"]); self.assertTrue(d["scientific_cell_values_equal"] and d["formula_functionally_equivalent"] and d["canonical_preserved"])

    def test_16_scale_gate_is_conservative(self):
        s=json.loads((OUT/"scale-readiness.json").read_text(encoding="utf-8"))
        self.assertEqual(s["decision"],"KEEP_BATCH_SIZE_10"); self.assertFalse(s["automatic_scale"])
        self.assertEqual(self.summary["decision"],"GO_NEXT_BATCH"); self.assertEqual(self.summary["scientific_pass"],"PROHIBITED")

    def test_17_manifest_hashes_and_lf_normalization(self):
        manifest=json.loads((OUT/"manifest.json").read_text(encoding="utf-8"))
        for name,m in manifest.items():
            target=OUT/name; self.assertTrue(target.exists()); self.assertEqual(m["hash_basis"],"NORMALIZED_LF")
            self.assertEqual(hashlib.sha256(lf(target)).hexdigest(),m["sha256"]); self.assertEqual(len(lf(target)),m["bytes"])

    def test_18_workbook_integrity_hashes_and_sheets(self):
        with zipfile.ZipFile(WORKBOOK) as z:
            self.assertIsNone(z.testzip()); xml=z.read("xl/workbook.xml").decode("utf-8")
            for name in ["Resumo","Seleção","Registros","Appraisal","Versões","Red Team","Proveniência","Revisão humana"]: self.assertIn(f'name="{name}"',xml)
        a=json.loads((OUT/"workbook-artifact.json").read_text(encoding="utf-8"))
        self.assertEqual(hashlib.sha256(WORKBOOK.read_bytes()).hexdigest(),a["binary_sha256"]); self.assertEqual(semantic_sha256(WORKBOOK),a["semantic_sha256"])

if __name__=="__main__": unittest.main()
