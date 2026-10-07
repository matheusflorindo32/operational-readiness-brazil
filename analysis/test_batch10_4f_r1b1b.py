import csv,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'batch10_4f_r1b1b'
def rows(n):
 with (O/n).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_packet_schema_and_counts():
 x=rows('CONSOLIDATED_16_REFERENCE_EVIDENCE_PACKETS.csv');assert len(x)==16;assert len({r['Evidence_ID'] for r in x})==16
 assert all(r['Packet_Completion'] for r in x)
def test_result_ids_and_locators_unique():
 x=rows('CONSOLIDATED_RESULT_LEVEL_EVIDENCE_LEDGER.csv');assert len({r['Result_ID'] for r in x})==len(x);assert all(r['Paragraph_or_Locator'] for r in x)
def test_no_force_and_cohort_protection():
 m=json.loads((O/'BATCH10_4F_R1B1B_MANIFEST.json').read_text());assert m['forced_semantic_links']==0
 assert 'independent cohort count=1' in next(r for r in rows('REFERENCE_COHORT_RELATION_FINAL.csv') if r['Evidence_ID']=='EV-1473')['Cohort_Relation']
