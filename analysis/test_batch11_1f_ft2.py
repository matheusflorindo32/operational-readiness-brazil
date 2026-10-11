import csv,hashlib,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'batch11_1f_ft2'
E={'TIER_AB_FULLTEXT_RESCUE_MASTER.csv','LAWFUL_FULLTEXT_SOURCE_LOG.csv','FULLTEXT_IDENTITY_VALIDATION.csv','FULLTEXT_RESCUE_OUTCOME.csv','EXTERNAL_EVIDENCE_ID_ASSIGNMENT_FT2.csv','RESULT_LOCATED_EXTERNAL_FT2.csv','RESULT_LOCATOR_AUDIT_FT2.csv','DESIGN_CLASSIFICATION_FT2.csv','APPRAISAL_FT2.csv','INTEGRITY_FT2.csv','STUDY_FAMILY_FT2.csv','TRANSFERABILITY_FT2.csv','NULL_RESULT_AUDIT_FT2.csv','CONTRADICTORY_EVIDENCE_FT2.csv','INCREMENTAL_VALUE_FT2.csv','CLAIM_ELIGIBILITY_FT2.csv','PROVISIONAL_EXTERNAL_CLAIMS_FT2.csv','RED_TEAM_FT2.csv','CONSOLIDATED_EXTERNAL_HUMAN_REVIEW_QUEUE.csv','REFERENCE_PROJECTION_FT2.csv','WORD_DENSITY_PROJECTION_FT2.csv','6500_WORD_SUFFICIENCY_DIAGNOSIS.csv','BATCH11_1F_FT2_MANIFEST.json','BATCH11_1F_FT2_REPORT.md'}
def rows(n):
 with (O/n).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
def h(p):return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
class FT2(unittest.TestCase):
 def test_artifacts_and_hashes(self):
  self.assertEqual({p.name for p in O.iterdir() if p.is_file()},E)
  m=json.loads((O/'BATCH11_1F_FT2_MANIFEST.json').read_text(encoding='utf8'))
  self.assertEqual(m['gate'],'EXTERNAL_FULLTEXT_RESCUE_PASS');self.assertEqual(m['qa']['tier_ab_total'],15);self.assertEqual(m['qa']['total_ab_full_texts_verified'],14)
  self.assertTrue(all(h(O/x['file'])==x['sha256'] for x in m['outputs']))
 def test_identity_and_no_automatic_promotion(self):
  a=rows('FULLTEXT_IDENTITY_VALIDATION.csv'); self.assertEqual(len(a),15);self.assertEqual(sum(x['Identity_Status']=='FULL_TEXT_IDENTITY_CONFIRMED' for x in a),14);self.assertEqual(sum(x['Conflict_Accepted']=='YES' for x in a),0)
  e=rows('CLAIM_ELIGIBILITY_FT2.csv'); self.assertTrue(all(x['Claim_Ready']=='NO' for x in e));self.assertEqual(len([x for x in e if x['Evidence_ID']]),8)
 def test_queue_and_controls(self):
  q=rows('CONSOLIDATED_EXTERNAL_HUMAN_REVIEW_QUEUE.csv');self.assertEqual(len(q),8);self.assertTrue(all(not x['Decision'] and not x['Reviewer'] and not x['Date'] for x in q))
  master=rows('TIER_AB_FULLTEXT_RESCUE_MASTER.csv');self.assertEqual(sum(x['Result_Located']=='YES' for x in master),14);self.assertTrue(all(x['Claim_Ready']=='NO' for x in master))
if __name__=='__main__':unittest.main()
