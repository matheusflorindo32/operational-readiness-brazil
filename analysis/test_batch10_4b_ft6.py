import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4b'/'ft6'
def rows(n):
    with (OUT/n).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def test_all_medium_are_screened_once():
    r=rows('MEDIUM109_INCREMENTAL_VALUE_SCREEN.csv'); assert len(r)==109 and len({x['Evidence_ID'] for x in r})==109
    assert {x['Selection_Decision'] for x in r} <= {'MEDIUM_TARGETED_REVIEW_REQUIRED','MEDIUM_DEFER','MEDIUM_LOW_INCREMENTAL_VALUE_AFTER_GAP_ANALYSIS'}
def test_selected_queue_is_gap_linked():
    r=rows('TARGETED_MEDIUM_REVIEW_QUEUE.csv'); assert all(x['Claim_ID'] and x['Gap_Severity'] and x['Selection_Rationale'] for x in r)
    assert all(x['Next_Action']=='FT7 lawful full-text access only' for x in r)
def test_manifest_preserves_governance():
    m=json.loads((OUT/'BATCH10_4B_FT6_MANIFEST.json').read_text(encoding='utf-8')); assert m['medium_assessed']==109
    assert m['cef_v1']==m['zotero']==m['manuscript']=='UNCHANGED'
