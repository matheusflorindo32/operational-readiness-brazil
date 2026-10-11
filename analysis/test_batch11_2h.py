import csv, json, unittest, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'batch11_2h'

class Batch112HTests(unittest.TestCase):
    def rows(self, name):
        with (OUT / name).open(encoding='utf-8-sig', newline='') as handle:
            return list(csv.DictReader(handle))

    def test_required_artifacts_are_complete(self):
        required = {
            'FINAL_HUMAN_DECISIONS_11_2.csv', 'EV1486_FINAL_RESULT_AUDIT.csv',
            'EV1492_FINAL_RESULT_AUDIT.csv', 'EV1492_INTERNAL_SOURCE_CONSISTENCY_AUDIT.csv',
            'FINAL_HOLD_RESOLUTION.csv', 'FINAL_CLAIM_READY_LEDGER_POST_HUMAN.csv',
            'FINAL_SENTENCE_PROVENANCE_POST_HUMAN.csv', 'FINAL_STATISTICAL_AUDIT_POST_HUMAN.csv',
            'FINAL_COHORT_AUDIT_POST_HUMAN.csv', 'FINAL_RED_TEAM_POST_HUMAN.md',
            'International_v1.3-FINAL-SCIENTIFIC-FREEZE.docx',
            'International_v1.3-FINAL-SCIENTIFIC-FREEZE.md',
            'FULL_MANUSCRIPT_FINAL_FREEZE_MANIFEST.json', 'BATCH11_2H_REPORT.md'
        }
        self.assertEqual(required, {path.name for path in OUT.iterdir() if path.is_file()})

    def test_only_two_authorized_human_decisions(self):
        rows = self.rows('FINAL_HUMAN_DECISIONS_11_2.csv')
        self.assertEqual(2, len(rows))
        self.assertEqual(['EV-1486', 'EV-1492'], [row['Evidence_ID'] for row in rows])
        self.assertTrue(all(row['Human_Decision'] == 'CONFIRM_BOUNDED_SUPPORT' for row in rows))
        self.assertTrue(all(row['Human_Reviewer'] == 'Matheus Florindo de Deus' for row in rows))
        self.assertTrue(all(row['Human_Review_Date'] == '2026-10-10' for row in rows))

    def test_holds_and_claims_resolve_deterministically(self):
        holds = self.rows('FINAL_HOLD_RESOLUTION.csv')
        self.assertEqual(2, len(holds))
        self.assertTrue(all(row['Post_Status'] == 'CLAIM_READY_PASS' and row['Unresolved'] == 'NO' for row in holds))
        claims = self.rows('FINAL_CLAIM_READY_LEDGER_POST_HUMAN.csv')
        self.assertEqual(20, len(claims))
        self.assertTrue(all(row['Claim_Ready'] == 'YES' for row in claims))
        self.assertTrue(all(row['Freeze_Status'] == 'FROZEN_FINAL_SCIENTIFIC_AUDIT' for row in claims))

    def test_result_boundaries_and_provenance(self):
        ev1486 = self.rows('EV1486_FINAL_RESULT_AUDIT.csv')
        self.assertEqual(1, len(ev1486))
        self.assertIn('724', ev1486[0]['Population'])
        self.assertIn('18.4', ev1486[0]['Exact_Results'])
        ev1492 = self.rows('EV1492_FINAL_RESULT_AUDIT.csv')
        self.assertEqual(1, len(ev1492))
        self.assertIn('18', ev1492[0]['Participant_Flow'] + ' ' + ev1492[0]['Completer_Results'] + ' ' + ev1492[0]['Null_or_Nonsignificant_Results'])
        self.assertIn('11', ev1492[0]['Participant_Flow'] + ' ' + ev1492[0]['Completer_Results'] + ' ' + ev1492[0]['Null_or_Nonsignificant_Results'])
        self.assertIn('statistically significant deterioration', ev1492[0]['Null_or_Nonsignificant_Results'].lower())
        source = self.rows('EV1492_INTERNAL_SOURCE_CONSISTENCY_AUDIT.csv')
        self.assertEqual(5, len(source))
        self.assertTrue(all(row['Status'] == 'PASS' for row in source))
        provenance = self.rows('FINAL_SENTENCE_PROVENANCE_POST_HUMAN.csv')
        self.assertEqual(34, len(provenance))
        self.assertTrue(all(row['Provenance_Chain'] == 'COMPLETE' for row in provenance))
        self.assertTrue(any(row['Evidence_IDs'] == 'EV-1486' and row['Reference_Numbers'] == '21' for row in provenance))
        self.assertTrue(any(row['Evidence_IDs'] == 'EV-1492' and row['Reference_Numbers'] == '24' for row in provenance))

    def test_statistical_and_cohort_guards(self):
        stats = self.rows('FINAL_STATISTICAL_AUDIT_POST_HUMAN.csv')
        self.assertEqual(6, len(stats))
        self.assertTrue(all(row['Audit'] == 'STATISTIC_MATCH' for row in stats))
        cohort = self.rows('FINAL_COHORT_AUDIT_POST_HUMAN.csv')
        self.assertTrue(all(row['Double_Counting'] == 'NO' for row in cohort))
        self.assertTrue(any(row['Evidence_IDs'] == 'EV-1492' and 'No shared dataset identified' in row['Finding'] for row in cohort))

    def test_manifest_text_and_ooxml(self):
        manifest = json.loads((OUT / 'FULL_MANUSCRIPT_FINAL_FREEZE_MANIFEST.json').read_text(encoding='utf-8'))
        self.assertEqual('FULL_MANUSCRIPT_FINAL_SCIENTIFIC_AUDIT_PASS', manifest['gate'])
        self.assertEqual('FULL_MANUSCRIPT_SCIENTIFIC_FREEZE_COMPLETE', manifest['freeze'])
        self.assertEqual('GO_FULL_LENGTH_TARGET_JOURNAL_SELECTION', manifest['next_gate'])
        import hashlib
        for output in manifest['outputs']:
            payload = (OUT / output['file']).read_bytes().replace(b'\r\n', b'\n')
            self.assertEqual(output['sha256'], hashlib.sha256(payload).hexdigest(), output['file'])
        qa = manifest['qa']
        self.assertEqual('2/2', qa['human_holds_resolved'])
        for field in ('unresolved_central_claims', 'unsupported_central_claims', 'orphan_references', 'duplicate_doi', 'cohort_double_counting', 'ev1379_support_use', 'contradictory_support_use', 'brazil_direct_inflation', 'material_scientific_drift', 'unauthorized_cef_mutation', 'unauthorized_zotero_mutation'):
            self.assertEqual(0, qa[field], field)
        with zipfile.ZipFile(OUT / 'International_v1.3-FINAL-SCIENTIFIC-FREEZE.docx') as docx:
            self.assertIsNone(docx.testzip())
            self.assertIn('word/document.xml', docx.namelist())
        text = (OUT / 'International_v1.3-FINAL-SCIENTIFIC-FREEZE.md').read_text(encoding='utf-8')
        self.assertIn('PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED', text)
        self.assertIn('Claim-Ready YES after named human adjudication', text)
        self.assertIn('724 police recruits from 15 Massachusetts academies', text)
        self.assertIn('18 male candidates started and 11 completed the course', text)
        self.assertIn('did not show statistically significant deterioration', text)
        self.assertNotIn('caffeine reverses sleep deprivation', text.lower())

if __name__ == '__main__':
    unittest.main()
