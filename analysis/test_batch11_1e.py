import csv,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'batch11_1e'
class Batch111ETests(unittest.TestCase):
 def test_gate_and_scope(self):
  m=json.loads((OUT/'BATCH11_1E_MANIFEST.json').read_text(encoding='utf-8'))
  self.assertEqual(m['gate'],'DEEP_INTERNAL_EVIDENCE_EXPANSION_PASS')
  self.assertEqual(m['word_target_gate'],'INTERNAL_EVIDENCE_INSUFFICIENT_FOR_6500_WORD_TARGET')
  self.assertEqual(m['qa']['canonical_universe'],1484)
  self.assertEqual(m['qa']['new_supporting_admitted'],0)
  self.assertEqual(m['qa']['claim_ready_promotions'],0)
  self.assertEqual(m['qa']['cef_mutation'],0)
  self.assertEqual(m['qa']['zotero_mutation'],0)
 def test_result_and_contradictory_guards(self):
  with (OUT/'RESULT_LOCATED_EXPANSION_MASTER.csv').open(encoding='utf-8-sig') as f:r=list(csv.DictReader(f))
  self.assertTrue(all(x['Evidence_ID'] and x['Result_ID'] and x['Source_Locator'] for x in r))
  with (OUT/'CONTRADICTORY_EVIDENCE_EXPANSION.csv').open(encoding='utf-8-sig') as f:c=list(csv.DictReader(f))
  self.assertEqual({x['Evidence_ID'] for x in c},{'EV-0052','EV-0140','EV-1066'})
  self.assertTrue(all(x['Support_Use']=='0' for x in c))
if __name__=='__main__':unittest.main()
