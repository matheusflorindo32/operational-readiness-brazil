from pathlib import Path
import csv,json,hashlib
O=Path('batch11_0b')
def rows(n):
 with (O/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def h(p):
 b=p.read_bytes()
 if p.suffix.lower() in {'.csv','.json','.md'}:b=b.replace(b'\r\n',b'\n')
 return hashlib.sha256(b).hexdigest()
m=json.loads((O/'BATCH11_0B_MANIFEST.json').read_text(encoding='utf8'))
x=rows('FULL_MANUSCRIPT_HUMAN_DECISION_LEDGER.csv');assert len(x)==26==len({r['Decision_ID'] for r in x})
assert all(r['Result_ID']==f"{r['Evidence_ID']}-11A-R01" for r in x)
assert all(not r[k] for r in x for k in ['HUMAN_DECISION','HUMAN_RATIONALE','HUMAN_REVIEWER','HUMAN_REVIEW_DATE'])
assert all(r['Integrity_Status']=='INTEGRITY_EXTERNAL_RECHECK_PENDING' and r['Prohibited_Inference'] for r in x)
assert sum(r['Null_Result']=='YES' for r in x)>0
assert all(r['Domain']!='other' for r in x)
claims=rows('PROVISIONAL_EXPANSION_CLAIM_LIBRARY.csv')
assert all(r['Claim_Status']=='PROVISIONAL_EXPANSION_CLAIM' and r['Claim_Ready']=='NO' and r['Human_Adjudication']=='PENDING' and r['Result_ID']==f"{r['Evidence_ID']}-11A-R01" and r['Locator'] for r in claims)
b=rows('BRAZIL_EXPANSION_STATUS.csv')[0];assert b['Gate']=='BRAZIL_EXPANSION_INSUFFICIENT' and b['Brazil_Direct_Inflation']=='0'
for n,expected in m['artifact_sha256'].items():assert h(O/n)==expected,n
print('BATCH11_0B tests PASS',len(x),len(claims))
