import csv,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_hr009_scope_comparison_and_overlap():
 q=rows(R/'batch10_4d'/'FINAL_HUMAN_REVIEW_QUEUE.csv');t=next(x for x in q if x['Review_ID']=='HR-009');assert t['HUMAN_DECISION']=='KEEP_CURRENT';assert next(x for x in q if x['Review_ID']=='HR-010')['HUMAN_DECISION']==''
 c=rows(R/'batch10_4e'/'HR009_REPLACEMENT_COMPARISON.csv');assert len(c)==18 and {x['Final_Classification'] for x in c}=={'KEEP_CURRENT'}
 o=rows(R/'batch10_4e'/'HR009_OVERLAP_COHORT_AUDIT.csv')[0];assert o['Overlap_Status']=='REVIEW_LEVEL_OVERLAP_WITH_PRIMARY_STUDIES' and o['Decision']=='DO_NOT_PROMOTE_OR_ADD'
 r=rows(R/'batch10_4e'/'HR009_HUMAN_DECISION_RECORD.csv')[0];assert r['Final_Reference_Freeze']=='NO'
 m=json.loads((R/'batch10_4d'/'BATCH10_4D_MANIFEST.json').read_text());assert m['human_adjudication_updates']['HR-009']['decision']=='KEEP_CURRENT'