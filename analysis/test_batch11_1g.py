import csv
import json
import re
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'batch11_1g'

class Batch111GTests(unittest.TestCase):
    def read_csv(self, name):
        with (OUT / name).open(encoding='utf-8-sig', newline='') as handle:
            return list(csv.DictReader(handle))

    def test_required_outputs_and_manifest_hashes(self):
        required = {
            'International_v1.1-FULL-MANUSCRIPT-EXPANDED.docx',
            'International_v1.1-FULL-MANUSCRIPT-EXPANDED.md',
            'FULL_MANUSCRIPT_V1_1_ACTIVE_REFERENCES.csv',
            'FULL_MANUSCRIPT_V1_1_CLAIM_TO_TEXT_MATRIX.csv',
            'FULL_MANUSCRIPT_V1_1_SENTENCE_LEVEL_PROVENANCE.csv',
            'FULL_MANUSCRIPT_V1_1_STUDY_CHARACTERISTICS.csv',
            'FULL_MANUSCRIPT_V1_1_DOMAIN_SYNTHESIS.csv',
            'FULL_MANUSCRIPT_V1_1_NULL_RESULT_AUDIT.csv',
            'FULL_MANUSCRIPT_V1_1_COHORT_AUDIT.csv',
            'FULL_MANUSCRIPT_V1_1_TRANSFERABILITY_MATRIX.csv',
            'FULL_MANUSCRIPT_V1_1_LIMITATIONS_MATRIX.csv',
            'FULL_MANUSCRIPT_V1_1_ORPHAN_REFERENCE_AUDIT.csv',
            'FULL_MANUSCRIPT_V1_1_SCIENTIFIC_DRIFT_AUDIT.csv',
            'WORD_COUNT_AND_PAGE_PROJECTION_V1_1.csv',
            'V1_0_TO_V1_1_CHANGELOG.md',
            'BATCH11_1G_MANIFEST.json',
            'BATCH11_1G_REPORT.md',
        }
        self.assertEqual(required, {p.name for p in OUT.iterdir() if p.is_file()})
        manifest = json.loads((OUT / 'BATCH11_1G_MANIFEST.json').read_text(encoding='utf-8'))
        self.assertEqual(28, manifest['qa']['active_references'])
        self.assertEqual(0, manifest['qa']['automatic_claim_ready'])
        self.assertEqual(0, manifest['qa']['new_search'])

    def test_claims_references_and_word_count(self):
        active = self.read_csv('FULL_MANUSCRIPT_V1_1_ACTIVE_REFERENCES.csv')
        self.assertEqual(28, len(active))
        self.assertEqual(set(range(1, 29)), {int(row['Citation_Number']) for row in active})
        claims = self.read_csv('FULL_MANUSCRIPT_V1_1_CLAIM_TO_TEXT_MATRIX.csv')
        self.assertTrue({'RC-EXP3-INT-PHYS-01','RC-EXP3-INT-PHYS-02','RC-EXP3-INT-SLEEP-01','RC-EXP3-INT-PHYS-03'}.issubset({row['Claim_ID'] for row in claims}))
        self.assertTrue(all(row['Claim_Ready'] == 'NO' for row in claims))
        words = self.read_csv('WORD_COUNT_AND_PAGE_PROJECTION_V1_1.csv')
        total = int(next(row['Words'] for row in words if row['Section'] == 'Body total excluding abstract and references'))
        self.assertGreaterEqual(total, 4012)
        self.assertLessEqual(total, 4432)

    def test_reference_and_integrity_guards(self):
        audit = self.read_csv('FULL_MANUSCRIPT_V1_1_ORPHAN_REFERENCE_AUDIT.csv')
        self.assertTrue(all(row['Status'] == 'PASS' for row in audit))
        drift = self.read_csv('FULL_MANUSCRIPT_V1_1_SCIENTIFIC_DRIFT_AUDIT.csv')
        self.assertTrue(all(row['Status'] == 'PASS' for row in drift))
        text = (OUT / 'International_v1.1-FULL-MANUSCRIPT-EXPANDED.md').read_text(encoding='utf-8')
        self.assertIn('PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED', text)
        self.assertIn('Potentially contradictory records EV-0052, EV-0140, and EV-1066 remain unadjudicated and are not used as support.', text)
        self.assertIn('Integrity-blocked EV-1379 is not used.', text)

    def test_docx_is_valid_ooxml(self):
        with zipfile.ZipFile(OUT / 'International_v1.1-FULL-MANUSCRIPT-EXPANDED.docx') as package:
            self.assertIsNone(package.testzip())
            self.assertIn('word/document.xml', package.namelist())

if __name__ == '__main__':
    unittest.main()

