import csv, hashlib, json, unittest, zipfile
from pathlib import Path
from docx import Document

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch11_4'
def csha(p): return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()

class Batch114Tests(unittest.TestCase):
    def test_artifact_set(self):
        expected={'International_v1.4-JOH-EDITORIAL-ADAPTED.docx','International_v1.4-JOH-EDITORIAL-ADAPTED.md','JOH_TITLE_AUDIT.csv','JOH_STRUCTURED_ABSTRACT_AUDIT.csv','JOH_ABSTRACT_PROVENANCE_AUDIT.csv','JOH_KEYWORDS_FINAL.csv','JOH_KEY_POINTS.md','JOH_SECTION_MAPPING.csv','JOH_REFERENCE_STYLE_CONVERSION.csv','JOH_TABLE_FIGURE_ASSESSMENT.csv','JOH_TITLE_PAGE_DRAFT.docx','JOH_DECLARATIONS_DRAFT.md','JOH_CREDIT_DRAFT.csv','JOH_DATA_AVAILABILITY_DRAFT.md','JOH_REPOSITORY_DISCLOSURE_AUDIT.md','JOH_AI_DISCLOSURE_DRAFT.md','JOH_REPORTING_GUIDELINE_FINAL_AUDIT.md','JOH_COVER_LETTER_DRAFT.md','JOH_SUBMISSION_REQUIREMENT_CHECKLIST.csv','JOH_HUMAN_INPUT_QUEUE.csv','JOH_EDITORIAL_CHANGELOG.csv','JOH_SCIENTIFIC_FREEZE_DIFF.csv','JOH_FINAL_WORD_COUNT.csv','JOH_DOCX_VALIDATION_REPORT.md','BATCH11_4_MANIFEST.json','BATCH11_4_REPORT.md'}
        self.assertEqual({p.name for p in OUT.iterdir() if p.is_file()},expected)
    def test_manifest_scientific_guards(self):
        m=json.loads((OUT/'BATCH11_4_MANIFEST.json').read_text(encoding='utf-8')); q=m['qa']
        self.assertEqual(m['gate'],'JOH_EDITORIAL_ADAPTATION_PASS'); self.assertEqual(q['central_claims_preserved'],'20/20')
        self.assertTrue(all(q[k]==0 for k in ['evidence_role_mutations','statistical_mutations','causal_mutations','transferability_mutations','new_scientific_references','removed_scientific_references','duplicate_doi','orphan_references','cef_mutation','zotero_mutation','brazil_mutation','authorship_mutation']))
        self.assertEqual(m['input_freeze']['docx_sha256'],'f5886dd8e715ee5d4666213b5b59027e382185a3ae19ce7959417ce6fe672030')
        self.assertEqual(m['input_freeze']['markdown_sha256_canonical_lf'],csha(ROOT/'batch11_2h/International_v1.3-FINAL-SCIENTIFIC-FREEZE.md'))
    def test_limits_and_references(self):
        with (OUT/'JOH_FINAL_WORD_COUNT.csv').open(encoding='utf-8', newline='') as stream: rows=list(csv.DictReader(stream))
        self.assertTrue(all(r['Pass']=='YES' for r in rows))
        with (OUT/'JOH_REFERENCE_STYLE_CONVERSION.csv').open(encoding='utf-8', newline='') as stream: refs=list(csv.DictReader(stream))
        self.assertEqual(len(refs),28); self.assertTrue(all(r['Identity_Mutation']=='0' for r in refs))
        with (OUT/'JOH_KEYWORDS_FINAL.csv').open(encoding='utf-8', newline='') as stream: kws=list(csv.DictReader(stream))
        self.assertEqual(len(kws),6)
    def test_docx_ooxml_and_framework_guard(self):
        for name in ['International_v1.4-JOH-EDITORIAL-ADAPTED.docx','JOH_TITLE_PAGE_DRAFT.docx']:
            with zipfile.ZipFile(OUT/name) as z:
                self.assertIn('word/document.xml',z.namelist()); self.assertIsNone(z.testzip())
        text='\n'.join(p.text for p in Document(OUT/'International_v1.4-JOH-EDITORIAL-ADAPTED.docx').paragraphs)
        self.assertIn('PROPOSED SYNTHESIS FRAMEWORK',text); self.assertIn('NOT YET VALIDATED',text)
        self.assertIn('Objectives:',text); self.assertIn('What this study adds.',text)
    def test_human_items_are_unresolved(self):
        with (OUT/'JOH_HUMAN_INPUT_QUEUE.csv').open(encoding='utf-8', newline='') as stream: rows=list(csv.DictReader(stream))
        self.assertGreaterEqual(len(rows),8); self.assertTrue(all(r['Status']=='HUMAN_INPUT_REQUIRED' and not r['Human_Decision'] for r in rows))
        self.assertIn('HUMAN_AI_DISCLOSURE_APPROVAL_REQUIRED',(OUT/'JOH_AI_DISCLOSURE_DRAFT.md').read_text(encoding='utf-8'))

if __name__=='__main__': unittest.main()
