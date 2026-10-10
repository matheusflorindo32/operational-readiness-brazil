from pathlib import Path
import csv,json,hashlib
O=Path('batch10_5c')
expected=['FINAL_AUTHORSHIP_MASTER.csv','AUTHORSHIP_HUMAN_DECISION_LEDGER.csv','AFFILIATION_MASTER.csv','ORCID_VALIDATION.csv','CREDIT_HUMAN_ADJUDICATION.csv','CORRESPONDING_AUTHOR_DECISION.csv','FUNDING_DECLARATIONS.csv','COI_HUMAN_DECLARATION.csv','AI_USE_DISCLOSURE_AUDIT.csv','FRONTIERS_AI_DISCLOSURE_DRAFT.md','RBSO_AI_DISCLOSURE_DRAFT.md','DATA_AVAILABILITY_DECLARATIONS.csv','FRONTIERS_SCOPE_STATEMENT_DRAFT.md','FRONTIERS_APC_DECISION.csv','RBSO_BLINDING_AUDIT.csv','RBSO_OPEN_SCIENCE_FORM_WORKING.md','LANGUAGE_FINAL_APPROVAL.csv','AUTHOR_FINAL_APPROVAL_QUEUE.csv','FINAL_SUBMISSION_METADATA_HUMAN_QUEUE.csv','METADATA_SCIENTIFIC_DRIFT_AUDIT.csv','BATCH10_5C_MANIFEST.json','BATCH10_5C_REPORT.md']
assert all((O/x).exists() for x in expected)
m=json.loads((O/'BATCH10_5C_MANIFEST.json').read_text(encoding='utf8'));assert m['scientific_drift']==0 and not m['v018_generated']
for n,h in m['artifact_sha256'].items():
 data=(O/n).read_bytes()
 if (O/n).suffix.lower() in {'.csv','.md','.json'}:
  data=data.replace(b'\r\n',b'\n')
 assert hashlib.sha256(data).hexdigest()==h,n
rows=list(csv.DictReader((O/'CREDIT_HUMAN_ADJUDICATION.csv').open(encoding='utf8')));assert len(rows)==14 and all(not r['HUMAN_DECISION'] for r in rows)
assert 'FINAL_AUTHOR_AND_SUBMISSION_METADATA_AWAITING_HUMAN_INPUT' in (O/'BATCH10_5C_REPORT.md').read_text(encoding='utf8')
print('BATCH10_5C tests: PASS',len(expected),'artifacts; 14 CRediT roles; no human fact fabricated')
