import csv, hashlib, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'batch11_3'
FREEZE=ROOT/'batch11_2h'
class Batch113Tests(unittest.TestCase):
 def rows(self,n):
  with (OUT/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
 def test_required_outputs(self):
  expected={'FULL_LENGTH_JOURNAL_LONG_LIST.csv','FULL_LENGTH_JOURNAL_ELIGIBILITY_AUDIT.csv','CURRENT_AUTHOR_GUIDELINES_AUDIT.csv','ARTICLE_TYPE_COMPATIBILITY.csv','JOURNAL_INDEXING_VERIFICATION.csv','JOURNAL_APC_AUDIT.csv','JOURNAL_METRICS_VERIFICATION.csv','JOURNAL_INTEGRITY_SCREEN.csv','TOP5_JOURNAL_COMPARISON.csv','TOP3_JOURNAL_DEEP_FIT_AUDIT.csv','DESK_REJECTION_RISK_MATRIX.csv','MANUSCRIPT_TO_JOURNAL_REQUIREMENT_GAP.csv','TARGET_JOURNAL_HUMAN_DECISION_QUEUE.csv','JOURNAL_SELECTION_RED_TEAM.md','BATCH11_3_MANIFEST.json','BATCH11_3_REPORT.md'}
  self.assertEqual(expected,{p.name for p in OUT.iterdir() if p.is_file()})
 def test_live_audit_counts_and_queue(self):
  self.assertEqual(10,len(self.rows('FULL_LENGTH_JOURNAL_LONG_LIST.csv')))
  top=self.rows('TOP5_JOURNAL_COMPARISON.csv'); self.assertEqual(5,len(top));self.assertEqual(['Journal of Occupational Health','Occupational Medicine','Military Medicine'],[r['Journal'] for r in top[:3]])
  queue=self.rows('TARGET_JOURNAL_HUMAN_DECISION_QUEUE.csv');self.assertEqual(3,len(queue));self.assertTrue(all(not r['HUMAN_SELECTION'] and not r['Human_Reviewer'] and not r['Human_Selection_Date'] for r in queue))
 def test_article_type_guards(self):
  rows=self.rows('ARTICLE_TYPE_COMPATIBILITY.csv');jsams=next(r for r in rows if r['Journal']=='Journal of Science and Medicine in Sport')
  self.assertEqual('EXCLUDE_ARTICLE_TYPE_MISMATCH',jsams['Decision']);self.assertEqual('YES',jsams['Mislabeling_Risk'])
  elig=self.rows('FULL_LENGTH_JOURNAL_ELIGIBILITY_AUDIT.csv');self.assertTrue(all(r['Mini_Review_Reversion']=='PROHIBITED' and r['Systematic_Review_Mislabeling']=='PROHIBITED' for r in elig))
 def test_word_count_fit_and_nonmutation(self):
  gaps=self.rows('MANUSCRIPT_TO_JOURNAL_REQUIREMENT_GAP.csv')
  mm=next(r for r in gaps if r['Journal']=='Military Medicine' and r['Requirement']=='Word count');self.assertEqual('REDUCE_UP_TO_205_WORDS_LATER',mm['Gap'])
  joh=next(r for r in gaps if r['Journal']=='Journal of Occupational Health' and r['Requirement']=='Word count');self.assertEqual('NONE',joh['Gap'])
  manifest=json.loads((OUT/'BATCH11_3_MANIFEST.json').read_text(encoding='utf-8'))
  self.assertEqual(4205,manifest['manuscript_facts']['Body_Words']);self.assertEqual(28,manifest['manuscript_facts']['References']);self.assertEqual(11,manifest['manuscript_facts']['Rendered_Pages'])
  for n,key in [('International_v1.3-FINAL-SCIENTIFIC-FREEZE.docx','docx_sha256'),('International_v1.3-FINAL-SCIENTIFIC-FREEZE.md','markdown_sha256')]:self.assertEqual(manifest['manuscript_snapshot'][key],hashlib.sha256((FREEZE/n).read_bytes().replace(b'\r\n',b'\n')).hexdigest())
 def test_manifest_hashes_and_guards(self):
  manifest=json.loads((OUT/'BATCH11_3_MANIFEST.json').read_text(encoding='utf-8'))
  self.assertEqual('FULL_LENGTH_TARGET_JOURNAL_FIT_AUDIT_PASS',manifest['gate']);self.assertEqual('GO_TARGET_JOURNAL_HUMAN_SELECTION',manifest['next_gate'])
  for item in manifest['outputs']:self.assertEqual(item['sha256'],hashlib.sha256((OUT/item['file']).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),item['file'])
  qa=manifest['qa']
  for field in ('manuscript_scientific_mutations','claim_mutations','cef_mutations','zotero_mutations','brazil_mutations','human_selection_populated'):self.assertEqual(0,qa[field],field)
  self.assertEqual('3/3',qa['official_author_guideline_verification_top3']);self.assertEqual('3/3',qa['article_type_compatibility_top3'])
if __name__=='__main__':unittest.main()
