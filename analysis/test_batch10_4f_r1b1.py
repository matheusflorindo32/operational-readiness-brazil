import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4f_r1b1'
def rows(name):
    with (OUT/name).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_inventory_and_provenance_complete():
    assert len(rows('FINAL_16_REFERENCE_SOURCE_INVENTORY.csv'))==16
    assert len(rows('REFERENCE_SOURCE_PROVENANCE.csv'))==16
def test_locators_are_auditable_and_no_forcing():
    ledger=rows('RESULT_LEVEL_EVIDENCE_LEDGER.csv'); loc=rows('RESULT_SOURCE_LOCATOR_LEDGER.csv')
    assert len(ledger)==len(loc)
    assert all(x['Locator_Auditable']=='YES' for x in loc)
    manifest=json.loads((OUT/'BATCH10_4F_R1B1_MANIFEST.json').read_text(encoding='utf-8'))
    assert manifest['forced_semantic_links']==0 and manifest['blocked_evidence_used_as_support']==0
def test_cohort_and_null_history_preserved():
    overlap=rows('REFERENCE_COHORT_OVERLAP.csv')[0]
    assert overlap['Independent_Cohort_Count']=='1'
    assert {'EV-1473','EV-1474','EV-1479'} <= {x['Evidence_ID'] for x in rows('REFERENCE_NULL_RESULTS.csv')}
