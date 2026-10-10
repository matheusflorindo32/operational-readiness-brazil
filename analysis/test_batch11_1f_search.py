import csv,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'batch11_1f_search'
class SearchTests(unittest.TestCase):
 def test_search_guards(self):
  m=json.loads((O/'BATCH11_1F_SEARCH_MANIFEST.json').read_text(encoding='utf-8'))
  self.assertEqual(m['gate'],'EXTERNAL_EVIDENCE_STILL_INSUFFICIENT_FOR_6500_WORD_TARGET')
  self.assertEqual(m['qa']['claim_ready_promotions'],0)
  self.assertEqual(m['qa']['supporting_candidates'],0)
  self.assertGreater(m['qa']['raw_records'],0)
 def test_no_abstract_promotion(self):
  with (O/'NEW_EXTERNAL_RECORDS.csv').open(encoding='utf-8-sig') as f:r=list(csv.DictReader(f))
  self.assertTrue(all(x['Admission']=='ABSTRACT_ONLY_HOLD' and not x['Evidence_ID'] for x in r))
if __name__=='__main__':unittest.main()
