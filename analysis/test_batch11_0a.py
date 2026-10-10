from pathlib import Path
import csv,json,hashlib
O=Path('batch11_0a');m=json.loads((O/'BATCH11_0A_MANIFEST.json').read_text(encoding='utf8'));assert m['expected']==m['appraised']==57 and m['claim_ready_promotions']==0
for n,h in m['artifact_sha256'].items():
 b=(O/n).read_bytes();
 if (O/n).suffix.lower() in {'.csv','.json','.md'}:b=b.replace(b'\r\n',b'\n')
 assert hashlib.sha256(b).hexdigest()==h,n
x=list(csv.DictReader((O/'RESULT_LOCATED_57_MASTER.csv').open(encoding='utf8')));assert len(x)==57==len({r['Evidence_ID'] for r in x}) and all(r['Claim_Ready']=='NO' for r in x)
y=list(csv.DictReader((O/'PROVISIONAL_CLAIM_LIBRARY_57.csv').open(encoding='utf8')));assert all(r['Result_ID'].endswith('-11A-R01') and r['Claim_Ready']=='NO' for r in y)
print('BATCH11_0A tests PASS',len(x),len(y))
