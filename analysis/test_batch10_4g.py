import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4g'
def rows(name):
    with (OUT/name).open(encoding='utf-8-sig', newline='') as f:return list(csv.DictReader(f))
def test_reconstruction_claims_are_result_located_and_bounded():
    claims=rows('NEW_CLAIM_LIBRARY.csv')
    assert len(claims) == 9
    assert all(r['Result_ID'] and r['Source_Locator'] for r in claims)
    assert all(r['Evidence_ID'] != 'EV-1379' for r in claims)
    assert all(r['Cohort_Family'] for r in claims)
def test_inventory_preserves_integrity_hold_and_does_not_promote_insufficient_sources():
    inventory=rows('RECONSTRUCTION_EVIDENCE_INVENTORY.csv')
    hold=next(r for r in inventory if r['Evidence_ID']=='EV-1379')
    assert hold['Eligibility_for_Reconstruction']=='DO_NOT_USE'
    ready=rows('RECONSTRUCTION_READY_EVIDENCE.csv')
    assert ready
    assert all(r['Result_Level_Data_Available']=='YES' for r in ready)
    assert all(r['Evidence_ID']!='EV-1379' for r in ready)
def test_blueprint_manifest_and_null_result_controls():
    m=json.loads((OUT/'BATCH10_4G_MANIFEST.json').read_text(encoding='utf-8'))
    assert len(list(OUT.iterdir())) == 15
    assert m['gate']=='MAJOR_RECONSTRUCTION_BLUEPRINT_PASS'
    assert m['recommended_architecture']=='B_NARROWED_INTEGRATIVE_MANUSCRIPT'
    for key in ['title_only_support_promoted','blocked_evidence_support','source_insufficient_evidence_promoted','rejected_pmcid_reused','cohort_double_counting','null_suppression','unauthorized_cef_change','old_unsupported_sentence_restoration']:
        assert m[key]==0
    domains=rows('DOMAIN_VIABILITY_MATRIX.csv')
    shooting=next(r for r in domains if r['Domain']=='Shooting / tactical performance')
    assert shooting['Independent_Cohort_Count']=='1'
