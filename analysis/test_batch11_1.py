import csv
import json
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'batch11_1'

class Batch111Tests(unittest.TestCase):
    def test_manifest_and_required_outputs(self):
        manifest=json.loads((OUT/'BATCH11_1_MANIFEST.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['gate'],'FULL_MANUSCRIPT_RECONSTRUCTION_PASS')
        self.assertEqual(manifest['counts']['frozen_international_claims'],4)
        self.assertEqual(manifest['counts']['human_approved_expansion_claims'],12)
        self.assertEqual(manifest['controls']['claim_ready_promotions'],0)
        self.assertFalse(manifest['controls']['zotero_changed'])
        self.assertFalse(manifest['controls']['cef_v1_changed'])
        self.assertTrue((OUT/'International_v1.0-FULL-MANUSCRIPT-WORKING.docx').exists())
        self.assertTrue((OUT/'International_v1.0-FULL-MANUSCRIPT-WORKING.md').exists())

    def test_docx_and_reference_reconciliation(self):
        docx=OUT/'International_v1.0-FULL-MANUSCRIPT-WORKING.docx'
        with zipfile.ZipFile(docx) as z:
            self.assertIsNone(z.testzip())
            self.assertIn('word/document.xml',z.namelist())
        with (OUT/'FULL_MANUSCRIPT_ACTIVE_REFERENCES.csv').open(encoding='utf-8-sig') as f:
            refs=list(csv.DictReader(f))
        with (OUT/'FULL_MANUSCRIPT_CLAIM_TO_TEXT_MATRIX.csv').open(encoding='utf-8-sig') as f:
            claims=list(csv.DictReader(f))
        self.assertEqual(len(refs),20)
        self.assertEqual(len(claims),16)
        self.assertEqual(len({x['DOI'] for x in refs if x['DOI']}),len([x for x in refs if x['DOI']]))
        self.assertNotIn('EV-1379',{x['Evidence_ID'] for x in refs})
        self.assertNotIn('EV-0014',{x['Evidence_ID'] for x in refs})
        self.assertNotIn('EV-0799',{x['Evidence_ID'] for x in refs})

    def test_provenance_and_claim_limits(self):
        with (OUT/'SENTENCE_LEVEL_PROVENANCE.csv').open(encoding='utf-8-sig') as f:
            provenance=list(csv.DictReader(f))
        self.assertGreaterEqual(len(provenance),150)
        scientific=[x for x in provenance if x['Material_Scientific_Sentence']=='YES']
        self.assertGreater(len(scientific),0)
        self.assertTrue(all(x['Evidence_IDs'] and x['Result_IDs'] and x['Reference_Numbers'] for x in scientific))
        text=(OUT/'International_v1.0-FULL-MANUSCRIPT-WORKING.md').read_text(encoding='utf-8')
        self.assertIn('PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED',text)
        self.assertIn('Claim-Ready NO',text)
        self.assertIn('EV-1379 is not used',text)
        self.assertNotIn('validated readiness framework',text.lower())

if __name__=='__main__':
    unittest.main()
