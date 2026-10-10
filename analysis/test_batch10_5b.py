from pathlib import Path
import zipfile,csv,json,hashlib
OUT=Path('batch10_5b')
required=['International_v0.17-FRONTIERS-SPORTS-MINI-REVIEW.docx','Brazil_v0.17-RBSO-ENSAIO.docx','TARGET_SPECIFIC_GUIDELINE_SNAPSHOT.csv','EDITORIAL_CHANGE_LEDGER.csv','CLAIM_DRIFT_AUDIT.csv','REFERENCE_DRIFT_AUDIT.csv','ABSTRACT_COHERENCE_POST_FORMATTING.csv','CONCLUSION_COHERENCE_POST_FORMATTING.csv','FRAMEWORK_POST_FORMATTING_AUDIT.csv','NULL_RESULT_POST_FORMATTING_AUDIT.csv','WORD_COUNT_COMPLIANCE.csv','REFERENCE_STYLE_COMPLIANCE.csv','DECLARATION_REQUIREMENTS.csv','AUTHORSHIP_HUMAN_INPUT_QUEUE.csv','FRONTIERS_SPORTS_SUBMISSION_CHECKLIST.csv','RBSO_SUBMISSION_CHECKLIST.csv','BRAZIL_TRANSLATION_EQUIVALENCE_AUDIT.csv','VISUAL_QA_REPORT.md','BATCH10_5B_MANIFEST.json','BATCH10_5B_REPORT.md']
assert all((OUT/x).exists() for x in required)
for p in OUT.glob('*.docx'):
 with zipfile.ZipFile(p) as z: assert z.testzip() is None; assert 'word/document.xml' in z.namelist()
for p in OUT.glob('*.csv'):
 with p.open(encoding='utf8',newline='') as f: assert next(csv.reader(f))
m=json.loads((OUT/'BATCH10_5B_MANIFEST.json').read_text(encoding='utf8')); assert m['scientific_changes']==m['claim_changes']==m['reference_changes']==0
assert 'VISUAL_QA_PASS' in (OUT/'VISUAL_QA_REPORT.md').read_text(encoding='utf8')
print('BATCH10_5B tests: PASS',len(required),'artifacts')
