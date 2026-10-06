import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_hr003_only_authorized_queue_update():
    queue=rows(ROOT/'batch10_4d'/'FINAL_HUMAN_REVIEW_QUEUE.csv'); target=next(r for r in queue if r['Review_ID']=='HR-003')
    assert target['HUMAN_DECISION']=='MAINTAIN' and target['HUMAN_REVIEWER']=='Matheus Florindo de Deus' and target['HUMAN_REVIEW_DATE']=='2026-10-06'
    assert all(not r['HUMAN_DECISION'] for r in queue if r['Review_ID'] not in {'HR-002','HR-003','HR-004','HR-005'})
def test_hr003_fail_closed_manuscript_controls():
    audit=rows(ROOT/'batch10_4e'/'HR003_MANUSCRIPT_COMPLIANCE_AUDIT.csv'); assert len(audit)==2
    for r in audit:
        assert r['EV0140_Used_As_Support']=='NO' and r['Universal_High_Fat_Impairment_Claims']=='0' and r['Unsupported_Causal_Dietary_Claims']=='0'
        assert r['Temporal_Overgeneralization']=='0' and r['Outcome_Overgeneralization']=='0' and r['Limitation_Preserved']=='YES' and r['FCR_Candidate']=='NO'
