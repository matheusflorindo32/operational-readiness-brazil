import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'batch10_4b'/'ft7';IDS={'EV-0222','EV-0651','EV-0692','EV-0776','EV-0906'}
def rows(n):
    with (OUT/n).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def test_ft7_exactly_matches_authorized_queue():
    r=rows('MEDIUM5_ACCESS_RECOVERY_MASTER.csv');assert len(r)==5 and {x['Evidence_ID'] for x in r}==IDS
    assert all(x['Final_Access_Status'] for x in r)
def test_body_and_identity_ledgers_cover_all_records():
    for n in ['MEDIUM5_IDENTITY_VALIDATION.csv','MEDIUM5_BODY_VALIDATION.csv','MEDIUM5_APPRAISAL_READINESS.csv','MEDIUM5_INTEGRITY_SCREEN.csv']:
        assert {x['Evidence_ID'] for x in rows(n)}==IDS
    assert all(x['No_Shared_Unrelated_Source']=='YES' for x in rows('MEDIUM5_APPRAISAL_READINESS.csv'))
def test_manifest_preserves_governance():
    m=json.loads((OUT/'BATCH10_4B_FT7_MANIFEST.json').read_text(encoding='utf-8'));assert m['processed']==5
    assert m['cef_v1']==m['zotero']==m['manuscript']=='UNCHANGED'
