import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_hr006_authorized_scope_only():
 q=rows(ROOT/'batch10_4d'/'FINAL_HUMAN_REVIEW_QUEUE.csv');t=next(r for r in q if r['Review_ID']=='HR-006')
 assert (t['HUMAN_DECISION'],t['HUMAN_REVIEWER'],t['HUMAN_REVIEW_DATE'])==('KEEP_CURRENT','Matheus Florindo de Deus','2026-10-06')
 assert all(not r['HUMAN_DECISION'] for r in q if r['Review_ID'] in {'HR-007','HR-008','HR-009','HR-010'})
def test_hr006_comparison_complete_and_no_promotion():
 c=rows(ROOT/'batch10_4e'/'HR006_REPLACEMENT_COMPARISON.csv');assert len(c)==18 and {r['Dimension_Number'] for r in c}=={str(i) for i in range(1,19)} and {r['Final_Classification'] for r in c}=={'KEEP_CURRENT'}
 i=rows(ROOT/'batch10_4e'/'HR006_CLAIM_IMPACT.csv'); assert next(r for r in i if r['Claim_ID']=='INT-NUTRITION-CAUTIOUS')['Current_Wording']=='NOT PRESENT AS A SUPPORTING CLAIM IN V0.13.'
 r=rows(ROOT/'batch10_4e'/'HR006_HUMAN_DECISION_RECORD.csv')[0];assert r['Final_Reference_Freeze']=='NO' and 'Not promoted' in r['EV0426_Use']
 m=json.loads((ROOT/'batch10_4d'/'BATCH10_4D_MANIFEST.json').read_text(encoding='utf-8'));assert m['human_adjudication_updates']['HR-006']['decision']=='KEEP_CURRENT'
