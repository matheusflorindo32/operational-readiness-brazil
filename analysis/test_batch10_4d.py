import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'batch10_4d'

def rows(name):
    with (OUT/name).open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f))

def test_claim_and_reference_audit_counts():
    assert len(rows('FINAL_CLAIM_AUDIT.csv')) == 60
    assert len(rows('FINAL_REFERENCE_AUDIT.csv')) == 16
    assert len(rows('FINAL_REPLACEMENT_REVIEW.csv')) == 6
    assert len(rows('FINAL_CONTRADICTORY_DISCLOSURE_AUDIT.csv')) == 3

def test_only_authorized_hr002_hr004_human_fields_are_populated_and_blocked_evidence_is_not_support():
    queue=rows('FINAL_HUMAN_REVIEW_QUEUE.csv')
    hr002=next(r for r in queue if r['Review_ID']=='HR-002')
    assert hr002['HUMAN_DECISION']=='MAINTAIN'
    assert hr002['HUMAN_REVIEWER']=='Matheus Florindo de Deus'
    assert hr002['HUMAN_REVIEW_DATE']=='2026-10-06'
    hr003=next(r for r in queue if r['Review_ID']=='HR-003')
    assert hr003['HUMAN_DECISION']=='MAINTAIN'
    assert hr003['HUMAN_REVIEWER']=='Matheus Florindo de Deus'
    assert hr003['HUMAN_REVIEW_DATE']=='2026-10-06'
    hr004=next(r for r in queue if r['Review_ID']=='HR-004')
    assert hr004['HUMAN_DECISION']=='MAINTAIN'
    assert hr004['HUMAN_REVIEWER']=='Matheus Florindo de Deus'
    assert hr004['HUMAN_REVIEW_DATE']=='2026-10-06'
    for r in queue:
        if r['Review_ID'] not in {'HR-002','HR-003','HR-004','HR-005'}:
            assert all(not r[x] for x in ['HUMAN_DECISION','HUMAN_REVIEWER','HUMAN_REVIEW_DATE','HUMAN_RATIONALE'])
    assert all(r['Used_As_Support'] == 'NO' for r in rows('FINAL_CONTRADICTORY_DISCLOSURE_AUDIT.csv'))

def test_framework_and_reference_controls():
    reconciliation={r['Metric']:r['Value'] for r in rows('FINAL_REFERENCE_RECONCILIATION.csv')}
    assert reconciliation['duplicate_doi'] == '0'
    assert reconciliation['cited_but_missing'] == '0'
    assert reconciliation['listed_but_uncited'] == '0'
    assert reconciliation['blocked_evidence_used_as_support'] == '0'
    assert all(r['Decision'] == 'PASS' for r in rows('FINAL_LANGUAGE_OVERCLAIM_AUDIT.csv'))

def test_manifest_gate_and_no_v014():
    m=json.loads((OUT/'BATCH10_4D_MANIFEST.json').read_text(encoding='utf-8'))
    assert m['claims_audited'] == 60 and m['references_audited'] == 16
    assert m['v014_generated'] is False
    assert m['cef_v1'] == 'UNCHANGED' and m['zotero'] == 'UNCHANGED'
