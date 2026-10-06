import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_hr004_only_authorized_queue_update():
 q=rows(ROOT/'batch10_4d'/'FINAL_HUMAN_REVIEW_QUEUE.csv');t=next(r for r in q if r['Review_ID']=='HR-004')
 assert t['HUMAN_DECISION']=='MAINTAIN' and t['HUMAN_REVIEWER']=='Matheus Florindo de Deus' and t['HUMAN_REVIEW_DATE']=='2026-10-06'
 assert all(not r['HUMAN_DECISION'] for r in q if r['Review_ID'] not in {'HR-002','HR-003','HR-004','HR-005','HR-006','HR-007','HR-008'})
def test_hr004_bmi_controls():
 a=rows(ROOT/'batch10_4e'/'HR004_MANUSCRIPT_COMPLIANCE_AUDIT.csv');assert len(a)==2
 for r in a:
  assert r['EV1066_Used_As_Support']=='NO' and r['BMI_Global_Readiness_Proxy_Claims']=='0' and r['BMI_Causal_Performance_Claims']=='0'
  assert r['BMI_Body_Composition_Conflation']=='0' and r['Population_Overtransfer']=='0' and r['Limitation_Preserved']=='YES' and r['FCR_Candidate']=='NO'
