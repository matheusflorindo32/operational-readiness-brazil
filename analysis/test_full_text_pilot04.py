import csv, json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "reporting/full-text/2026-09-20/pilot-04"
EXPECTED = ["EV-0103","EV-1301","EV-1039","EV-0796","EV-0632","EV-0458","EV-0376","EV-0880","EV-0862","EV-0813"]

def rows(name):
    with (P/name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

class Pilot04Regression(unittest.TestCase):
    def test_selection_exact_and_deterministic(self):
        r=rows("selection-audit.csv")
        self.assertEqual([x["Evidence ID"] for x in r], EXPECTED)
        self.assertEqual(len(r),10)
        self.assertTrue(all(x["Acesso"]=="PMC_AVAILABLE" for x in r))

    def test_exclusions(self):
        text=(P/"pilot-records.csv").read_text(encoding="utf-8-sig")
        self.assertNotIn("FXC7ZY9R",text)
        self.assertNotIn("26159007",text)

    def test_human_gate_fail_closed(self):
        r=rows("pilot-records.csv")
        for x in r:
            self.assertEqual(x["Claim-Ready"],"NO")
            self.assertEqual(x["Status"],"HUMAN_REVIEW_REQUIRED")
            for k in ["Revisor humano","Data humana","Decisão humana","Justificativa humana","Confirmação humana"]:
                self.assertEqual((x[k] or "").strip(),"")

    def test_human_queue_40(self):
        r=rows("human-review-queue-pilots-01-04.csv")
        self.assertEqual(len(r),40)
        self.assertEqual(sum(1 for x in r if x["Piloto"]=="PILOT_04"),10)
        self.assertTrue(all(x["Claim-Ready"]=="NO" for x in r))

    def test_appraisal_and_red_team(self):
        a=rows("appraisal-domain-ledger.csv")
        self.assertEqual(len(a),89)
        self.assertEqual(set(x["Evidence ID"] for x in a),set(EXPECTED))
        rt=rows("red-team-ledger.csv")
        self.assertEqual(len(rt),10)
        self.assertTrue(all(x["overall"]=="PASS" for x in rt))

    def test_version_holds(self):
        r={x["Evidence ID"]:x for x in rows("versions-ledger.csv")}
        self.assertEqual(r["EV-0632"]["Comparação VOR"],"VOR_COMPARISON_PENDING")
        self.assertEqual(r["EV-0376"]["Comparação VOR"],"VOR_COMPARISON_PENDING")

    def test_manifest_and_summary(self):
        m=json.loads((P/"run-summary.json").read_text(encoding="utf-8"))
        self.assertEqual(m["human_review_queue_total"],40)
        self.assertEqual(m["claim_ready"],0)
        self.assertEqual(m["decision"],"HUMAN_REVIEW_PRIORITY")
        self.assertEqual(m["scale_readiness"],"KEEP_BATCH_SIZE_10")

    def test_workbook_artifact_metadata_fail_closed(self):
        w=json.loads((P/"workbook-artifact.json").read_text(encoding="utf-8"))
        self.assertEqual(w["binary_sha256"],"6aad700b8b35930c272ce86967a9d508295191303dececbdae352503004ef841")
        self.assertEqual(w["semantic_sha256"],"ce963365f3454b3afbc09fbe1d0fef6cf97a7f8aa085223611699a550d311598")
        self.assertFalse(w["repository_binary_present"])
        self.assertEqual(w["binary_publication_status"],"EXTERNAL_ARTIFACT_ONLY_CONNECTOR_BINARY_UPLOAD_UNSUPPORTED")

if __name__=="__main__":
    unittest.main()
