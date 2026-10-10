from pathlib import Path
import csv,json,hashlib
O=Path('batch11_0'); m=json.loads((O/'BATCH11_0_MANIFEST.json').read_text(encoding='utf8'))
assert m['canonical_records']==1484==m['canonical_unique_evidence_ids'] and m['scientific_mutations']==0 and not m['new_search_authorized']
r=list(csv.DictReader((O/'CANONICAL_1484_REASSESSMENT.csv').open(encoding='utf8')));assert len(r)==1484==len({x['Evidence_ID'] for x in r})
assert all(x['Claim_Ready']=='NO' for x in r)
for n,h in m['artifact_sha256'].items():
 b=(O/n).read_bytes();
 if (O/n).suffix.lower() in {'.csv','.md','.json'}:b=b.replace(b'\r\n',b'\n')
 assert hashlib.sha256(b).hexdigest()==h,n
print('BATCH11_0 tests: PASS',len(r),'canonical IDs;',m['result_located_packets'],'result-located candidates')
