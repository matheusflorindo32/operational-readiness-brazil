from pathlib import Path
import csv,json,hashlib,collections
O=Path('batch11_0c')
def rows(n):
 with (O/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def h(p):
 b=p.read_bytes()
 if p.suffix.lower() in {'.csv','.json','.md'}:b=b.replace(b'\r\n',b'\n')
 return hashlib.sha256(b).hexdigest()
m=json.loads((O/'BATCH11_0C_MANIFEST.json').read_text(encoding='utf8'))
x=rows('HUMAN_EXPANSION_DECISIONS_FINAL.csv');assert len(x)==26
assert collections.Counter(r['HUMAN_DECISION'] for r in x)=={'RETAIN_BOUNDED_SUPPORTING_CANDIDATE':12,'CONTEXTUAL_DISCUSSION_ONLY':12,'EXCLUDE_FROM_FULL_MANUSCRIPT':2}
assert all(r['HUMAN_REVIEWER']=='Matheus Florindo de Deus' and r['HUMAN_REVIEW_DATE']=='2026-10-10' and r['Claim_Ready']=='NO' for r in x)
assert all(r['Integrity_Status']=='INTEGRITY_EXTERNAL_RECHECK_PENDING' for r in x)
assert sum(r['Null_Result']=='YES' for r in x)==4
claims=rows('HUMAN_APPROVED_EXPANSION_CLAIM_LIBRARY.csv');assert len(claims)==12 and all(r['Claim_Status']=='HUMAN_APPROVED_EXPANSION_CLAIM' and r['Claim_Ready']=='NO' for r in claims)
assert len({r['Study_Family_ID'] for r in x})==26
assert rows('BRAZIL_EXPANSION_STATUS_POST_HUMAN.csv')[0]['Brazil_Direct_Inflation']=='0'
assert rows('INTERNATIONAL_FULL_MANUSCRIPT_VIABILITY_POST_HUMAN.csv')[0]['Next_Gate']=='GO_EXTERNAL_INTEGRITY_RECHECK_BEFORE_RECONSTRUCTION'
for n,v in m['artifact_sha256'].items():assert h(O/n)==v,n
print('BATCH11_0C tests PASS',len(x),len(claims))
