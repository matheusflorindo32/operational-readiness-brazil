import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'batch10_4f_r1b1a'
def rows(n):
 with (OUT/n).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_targets_and_identity_records_complete():
 assert len(rows('TARGETED_SOURCE_RECOVERY_LEDGER.csv'))==14
 assert len(rows('SOURCE_IDENTITY_VALIDATION.csv'))==14
def test_no_illegal_access_or_reference_growth():
 assert all(x['Illegal_Access']=='NO' for x in rows('LAWFUL_ACCESS_ROUTE_LEDGER.csv'))
 m=json.loads((OUT/'BATCH10_4F_R1B1A_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['forced_semantic_links']==0 and m['new_references_added']==0
def test_ev1474_legacy_pmcid_rejected_and_gov_source_present():
 assert rows('EV1474_IDENTITY_RECHECK.csv')[0]['Reported_PMCID'].startswith('PMC3382270')
 assert rows('EV1477_GOVERNMENT_SOURCE_AUDIT.csv')[0]['Access']=='VERIFIED_GOVERNMENT_SOURCE'
