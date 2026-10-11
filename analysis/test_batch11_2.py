import csv, json, unittest, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'batch11_2'
class Batch112Tests(unittest.TestCase):
    def rows(self,n):
        with (OUT/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
    def test_all_required_artifacts(self):
        required={'International_v1.2-FINAL-SCIENTIFIC-AUDIT.docx','International_v1.2-FINAL-SCIENTIFIC-AUDIT.md','FINAL_CLAIM_AUDIT.csv','FINAL_SENTENCE_LEVEL_AUDIT.csv','FINAL_STATISTICAL_AUDIT.csv','FINAL_REFERENCE_AUDIT_28.csv','FINAL_INTEGRITY_RECHECK_28.csv','FINAL_COHORT_OVERLAP_AUDIT.csv','FINAL_NULL_RESULT_AUDIT.csv','FINAL_CONTRADICTORY_EVIDENCE_AUDIT.csv','FINAL_CONTEXTUAL_ROLE_AUDIT.csv','FINAL_TRANSFERABILITY_AUDIT.csv','FINAL_CAUSAL_LANGUAGE_AUDIT.csv','FINAL_PROVENANCE_CHAIN_AUDIT.csv','FINAL_ABSTRACT_AUDIT.csv','FINAL_METHODS_AUDIT.csv','FINAL_RESULTS_SYNTHESIS_AUDIT.csv','FINAL_DISCUSSION_AUDIT.csv','FINAL_LIMITATIONS_AUDIT.csv','FINAL_CONCLUSION_AUDIT.csv','FINAL_SCIENTIFIC_DRIFT_AUDIT.csv','FINAL_CLAIM_READY_LEDGER.csv','SCIENTIFIC_AUDIT_CORRECTIONS_APPLIED.csv','NEW_HUMAN_DECISION_QUEUE.csv','FULL_MANUSCRIPT_SCIENTIFIC_FREEZE_MANIFEST.json','BATCH11_2_REPORT.md'}
        self.assertEqual(required,{p.name for p in OUT.iterdir() if p.is_file()})
    def test_reference_and_integrity_guards(self):
        refs=self.rows('FINAL_REFERENCE_AUDIT_28.csv'); integ=self.rows('FINAL_INTEGRITY_RECHECK_28.csv')
        self.assertEqual(28,len(refs));self.assertEqual(28,len(integ))
        self.assertTrue(all(x['Audit_Status']=='PASS' for x in refs))
        self.assertTrue(all(x['DOI_Identity_Status']=='MATCH' and x['Integrity_Status']=='INTEGRITY_CLEAR_CURRENT_CHECK' for x in integ))
    def test_claim_sentence_and_hold_integrity(self):
        claims=self.rows('FINAL_CLAIM_AUDIT.csv'); self.assertEqual(20,len(claims))
        self.assertEqual(18,sum(x['Claim_Status']=='CLAIM_READY_PASS' for x in claims));self.assertEqual(2,sum(x['Claim_Status']=='CLAIM_HOLD' for x in claims))
        self.assertTrue(all(x['Stored_Claim_Ready']=='NO' for x in claims))
        sentences=self.rows('FINAL_SENTENCE_LEVEL_AUDIT.csv'); material=[x for x in sentences if x['Material_Scientific_Sentence']=='YES']
        self.assertEqual(33,len(material)); self.assertTrue(all(x['Provenance_Chain']=='COMPLETE' for x in material))
        queue=self.rows('NEW_HUMAN_DECISION_QUEUE.csv');self.assertEqual(['EV-1486','EV-1492'],[x['Evidence_ID'] for x in queue]);self.assertTrue(all(not x['Human_Decision'] for x in queue))
    def test_protections_and_ooxml(self):
        contra=self.rows('FINAL_CONTRADICTORY_EVIDENCE_AUDIT.csv');self.assertTrue(all(x['Support_Use']=='0' for x in contra))
        cohort=self.rows('FINAL_COHORT_OVERLAP_AUDIT.csv');self.assertEqual('NO',cohort[0]['Double_Counting'])
        with zipfile.ZipFile(OUT/'International_v1.2-FINAL-SCIENTIFIC-AUDIT.docx') as z:self.assertIsNone(z.testzip());self.assertIn('word/document.xml',z.namelist())
        text=(OUT/'International_v1.2-FINAL-SCIENTIFIC-AUDIT.md').read_text(encoding='utf-8')
        self.assertIn('PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED',text);self.assertIn('uses 28 active working references',text);self.assertIn('doi:10.2147/NSS.S601666',text)
if __name__=='__main__':unittest.main()
