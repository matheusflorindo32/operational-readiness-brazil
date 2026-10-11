import csv,hashlib,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'batch11_1f_human'
E={'EXTERNAL_HUMAN_DECISIONS_FINAL.csv','HUMAN_APPROVED_EXTERNAL_EXPANSION_CLAIMS.csv','HUMAN_APPROVED_EXTERNAL_CONTEXTUAL_EVIDENCE.csv','POST_HUMAN_REFERENCE_PROJECTION.csv','POST_HUMAN_WORD_DENSITY_PROJECTION.csv','POST_HUMAN_DOMAIN_DENSITY.csv','POST_HUMAN_CLAIM_MAP.csv','POST_HUMAN_SUFFICIENCY_DIAGNOSIS.csv','BATCH11_1F_HUMAN_MANIFEST.json','BATCH11_1F_HUMAN_REPORT.md'}
def rows(n):
 with (O/n).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
def h(p):return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
class Human(unittest.TestCase):
 def test_artifacts_manifest(self):
  self.assertEqual({p.name for p in O.iterdir() if p.is_file()},E);m=json.loads((O/'BATCH11_1F_HUMAN_MANIFEST.json').read_text(encoding='utf8'));self.assertEqual(m['gate'],'EXTERNAL_EXPANSION_HUMAN_ADJUDICATION_PASS');self.assertEqual(m['qa']['human_decisions_completed'],8);self.assertTrue(all(h(O/x['file'])==x['sha256'] for x in m['outputs']))
 def test_authorized_decisions_only(self):
  d=rows('EXTERNAL_HUMAN_DECISIONS_FINAL.csv');self.assertEqual(len(d),8);self.assertEqual(sum(x['Human_Decision']=='ADMIT_NARROWLY' for x in d),4);self.assertEqual(sum(x['Human_Decision']=='RETAIN_CONTEXTUAL' for x in d),4);self.assertTrue(all(x['Human_Reviewer']=='Matheus Florindo de Deus' and x['Human_Review_Date']=='2026-10-10' for x in d));self.assertTrue(all(x['Claim_Ready']=='NO' for x in d))
 def test_claim_traceability(self):
  c=rows('HUMAN_APPROVED_EXTERNAL_EXPANSION_CLAIMS.csv');self.assertEqual([x['Claim_ID'] for x in c],['RC-EXP3-INT-PHYS-01','RC-EXP3-INT-PHYS-02','RC-EXP3-INT-SLEEP-01','RC-EXP3-INT-PHYS-03']);self.assertTrue(all(x['Result_ID'] and x['Source_Locator'] and x['Claim_Ready']=='NO' for x in c))
if __name__=='__main__':unittest.main()
