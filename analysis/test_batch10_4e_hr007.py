import csv,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_hr007_scope_and_comparison():
 q=rows(R/'batch10_4d'/'FINAL_HUMAN_REVIEW_QUEUE.csv');t=next(x for x in q if x['Review_ID']=='HR-007');assert t['HUMAN_DECISION']=='KEEP_CURRENT' and t['HUMAN_REVIEWER']=='Matheus Florindo de Deus'
 assert all(not x['HUMAN_DECISION'] for x in q if x['Review_ID'] in {})
 c=rows(R/'batch10_4e'/'HR007_REPLACEMENT_COMPARISON.csv');assert len(c)==18 and {x['Dimension_Number'] for x in c}=={str(i) for i in range(1,19)} and {x['Final_Classification'] for x in c}=={'KEEP_CURRENT'}
 i=rows(R/'batch10_4e'/'HR007_CLAIM_IMPACT.csv');assert next(x for x in i if x['Claim_ID']=='INT-FIREFIGHTER-SUPPLEMENT-SPECIFIC')['Current_Wording']=='NOT PRESENT AS A SUPPORTING CLAIM IN V0.13.'
 r=rows(R/'batch10_4e'/'HR007_HUMAN_DECISION_RECORD.csv')[0];assert r['Final_Reference_Freeze']=='NO' and 'Not promoted' in r['EV0521_Use']
 m=json.loads((R/'batch10_4d'/'BATCH10_4D_MANIFEST.json').read_text(encoding='utf-8'));assert m['human_adjudication_updates']['HR-007']['decision']=='KEEP_CURRENT'
