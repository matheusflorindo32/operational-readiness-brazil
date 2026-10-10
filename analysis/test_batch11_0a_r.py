from pathlib import Path
import csv,json,hashlib
O=Path('batch11_0a_r')
def rows(n):
 with (O/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def h(p):
 b=p.read_bytes()
 if p.suffix.lower() in {'.csv','.json','.md'}:b=b.replace(b'\r\n',b'\n')
 return hashlib.sha256(b).hexdigest()
m=json.loads((O/'BATCH11_0A_R_MANIFEST.json').read_text(encoding='utf8'))
master=rows('RESULT_LOCATED_57_MASTER_REPAIRED.csv'); assert len(master)==57==len({r['Evidence_ID'] for r in master})
assert len({r['Result_ID'] for r in master})==57
assert all(r['Result_ID']==f"{r['Evidence_ID']}-11A-R01" for r in master)
assert all(r['Locator'] and r['Exact_Result'] and r['Claim_Ready']=='NO' for r in master)
chain=rows('RESULT_LOCATOR_CHAIN_REPAIRED.csv');assert len(chain)==57 and all(r['Same_Evidence_Record']=='YES' and r['Locator_Exists']=='YES' for r in chain)
prot=rows('PROTOCOL_GUARD_REPAIRED.csv'); assert {r['Evidence_ID'] for r in prot if r['Protocol_Status']=='PROTOCOL_ONLY'}=={'EV-0161','EV-0195','EV-0311','EV-0529','EV-0641'}
q=rows('BATCH11_0A_HUMAN_REVIEW_QUEUE_REPAIRED.csv'); assert all(not r[x] for r in q for x in ['HUMAN_DECISION','HUMAN_RATIONALE','HUMAN_REVIEWER','HUMAN_REVIEW_DATE'])
assert all(r['Evidence_ID']+'-11A-R01'==r['Result_ID'] for r in q)
design={r['Evidence_ID']:r for r in rows('DESIGN_RECLASSIFICATION_REPAIRED.csv')}; domain={r['Evidence_ID']:r for r in rows('DOMAIN_RECLASSIFICATION_REPAIRED.csv')}
assert design['EV-0146']['Repaired_Design']=='RETROSPECTIVE_COHORT'; assert domain['EV-0146']['Repaired_Domain']=='musculoskeletal injury'
assert design['EV-0721']['Repaired_Design']=='RETROSPECTIVE_COHORT'; assert design['EV-0756']['Repaired_Design']=='RETROSPECTIVE_COHORT'
for n,expected in m['artifact_sha256'].items():assert h(O/n)==expected,n
print('BATCH11_0A_R tests PASS',len(master),len(q))
