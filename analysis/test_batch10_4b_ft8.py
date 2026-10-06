import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'batch10_4b'/'ft8'
def rows(n):
 with (OUT/n).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def test_all_mandated_domains_are_adjudicated_once():
 r=rows('DOMAIN_SATURATION_ADJUDICATION.csv');assert len(r)==17 and len({x['Domain'] for x in r})==17
 assert {x['Saturation_Status'] for x in r} <= {'SATURATED','SATURATED_WITH_ACCESS_LIMITATION','PARTIALLY_SATURATED','NOT_SATURATED','BLOCKED_BY_UNRESOLVED_CONTRADICTORY_EVIDENCE','BLOCKED_BY_ACCESS'}
def test_contradictions_and_access_limits_are_preserved():
 r=rows('UNRESOLVED_CONTRADICTORY_LEDGER.csv');assert {x['Evidence_ID'] for x in r}=={'EV-0052','EV-0140','EV-1066'}
 assert len(rows('ACCESS_LIMITATION_IMPACT.csv'))==3
def test_manifest_preserves_governance():
 m=json.loads((OUT/'BATCH10_4B_FT8_MANIFEST.json').read_text(encoding='utf-8'));assert m['domains']==17
 assert m['cef_v1']==m['zotero']==m['manuscript']=='UNCHANGED'
