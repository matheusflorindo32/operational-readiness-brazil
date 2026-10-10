import csv
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'batch11_1f_ft'
EXPECTED={
'EXTERNAL_55_PRIORITY_TRIAGE.csv','FULL_TEXT_RETRIEVAL_LOG.csv','FULL_TEXT_VERIFICATION.csv','EXTERNAL_EVIDENCE_ID_ASSIGNMENT_FINAL.csv','RESULT_LOCATED_EXTERNAL_FULLTEXT_MASTER.csv','RESULT_LOCATOR_AUDIT.csv','DESIGN_CLASSIFICATION_EXTERNAL_FULLTEXT.csv','APPRAISAL_EXTERNAL_FULLTEXT.csv','INTEGRITY_EXTERNAL_FULLTEXT.csv','STUDY_FAMILY_EXTERNAL_FULLTEXT.csv','TRANSFERABILITY_EXTERNAL_FULLTEXT.csv','NULL_RESULT_EXTERNAL_FULLTEXT_AUDIT.csv','CONTRADICTORY_EXTERNAL_FULLTEXT.csv','INCREMENTAL_VALUE_EXTERNAL.csv','CLAIM_ELIGIBILITY_EXTERNAL_FULLTEXT.csv','PROVISIONAL_EXTERNAL_EXPANSION_CLAIM_LIBRARY.csv','RED_TEAM_EXTERNAL_FULLTEXT.csv','WORD_DENSITY_EXTERNAL_FULLTEXT.csv','REFERENCE_PROJECTION_EXTERNAL_FULLTEXT.csv','HUMAN_MATERIALITY_EXTERNAL_FULLTEXT.csv','BATCH11_1F_FT_HUMAN_REVIEW_QUEUE.csv','ZOTERO_IMPORT_CANDIDATES.csv','EXTERNAL_FULLTEXT_6500_WORD_FEASIBILITY.csv','BATCH11_1F_FT_MANIFEST.json','BATCH11_1F_FT_REPORT.md'}

def read(name):
    with (OUT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

class ExternalFullTextTests(unittest.TestCase):
    def test_required_artifacts_and_manifest_hashes(self):
        self.assertEqual({p.name for p in OUT.iterdir() if p.is_file()},EXPECTED)
        manifest=json.loads((OUT/'BATCH11_1F_FT_MANIFEST.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['gate'],'EXTERNAL_FULLTEXT_APPRAISAL_PARTIAL')
        self.assertEqual(manifest['qa']['external_records'],55)
        self.assertEqual(manifest['qa']['automatic_claims'],0)
        self.assertEqual(manifest['qa']['claim_ready_promotions'],0)
        self.assertEqual(manifest['qa']['zotero_changes'],0)
        for item in manifest['outputs']:
            self.assertEqual(hashlib.sha256((OUT/item['file']).read_bytes()).hexdigest(),item['sha256'])
    def test_identity_and_promotion_guards(self):
        tri=read('EXTERNAL_55_PRIORITY_TRIAGE.csv')
        self.assertEqual(len(tri),55)
        self.assertEqual(sum(x['Primary_Identifier_Status']=='CORRECTED_DISCOVERY_REFERENCE_ID' for x in tri),41)
        master=read('RESULT_LOCATED_EXTERNAL_FULLTEXT_MASTER.csv')
        assigned=[x for x in master if x['Evidence_ID']]
        self.assertEqual(len(assigned),manifest['qa']['new_evidence_ids_assigned'])
        self.assertGreater(len(assigned),0)
        self.assertTrue(all(x['Result_ID']==x['Evidence_ID']+'-11F-FT-R01' for x in assigned))
        self.assertTrue(all(x['Claim_Ready']=='NO' for x in master))
        self.assertTrue(all(x['Admission_Status']!='ACTIVE_REFERENCE' for x in master))
    def test_locators_and_human_queue(self):
        loc=read('RESULT_LOCATOR_AUDIT.csv')
        assigned=[x for x in loc if x['Evidence_ID']]
        manifest=json.loads((OUT/'BATCH11_1F_FT_MANIFEST.json').read_text(encoding='utf-8'))
        self.assertEqual(len(assigned),manifest['qa']['new_result_ids'])
        self.assertTrue(all('BioC passage' in x['Source_Locator'] and x['Auditable']=='YES' for x in assigned))
        queue=read('BATCH11_1F_FT_HUMAN_REVIEW_QUEUE.csv')
        self.assertEqual(len(queue),manifest['qa']['new_evidence_ids_assigned'])
        self.assertTrue(all(not x['Human_Decision'] and not x['Human_Reviewer'] and not x['Human_Date'] for x in queue))

if __name__=='__main__':unittest.main()
