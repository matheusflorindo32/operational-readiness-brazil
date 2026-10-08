import csv, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'batch10_4f_r1c'

def rows(name):
    with (OUT/name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def test_r1c_applies_all_r1b2_actions_and_is_fail_closed():
    assert len(rows('R1C_DELETE_APPLICATION_LEDGER.csv')) == 123
    assert len(rows('R1C_NARROWING_APPLICATION_LEDGER.csv')) == 3
    assert len(rows('R1C_LIMITATION_APPLICATION_LEDGER.csv')) == 5
    post=rows('R1C_POSTBUILD_CLAIM_SUPPORT_MATRIX.csv')
    assert len(post) == 8
    assert all(r['Result_IDs'] and r['Source_Locators'] for r in post)
    assert all('PMC3382270' not in r['Source_Locators'] for r in post)

def test_r1c_manifest_records_major_reconstruction_without_freeze():
    m=json.loads((OUT/'BATCH10_4F_R1C_MANIFEST.json').read_text(encoding='utf-8'))
    assert m['gate'] == 'RECONCILED_V014_MAJOR_RECONSTRUCTION_REQUIRED'
    assert m['unsupported_active_scientific_sentences'] == 0
    assert m['reference_freeze_executed'] is False
    assert m['unauthorized_cef_v1_change'] == 0
    assert m['pdf_rendering_status'] == 'NOT_GENERATED_BUNDLED_LIBREOFFICE_UNAVAILABLE'

def test_r1c_v014_outputs_exist_and_v013_source_hashes_are_preserved():
    m=json.loads((OUT/'BATCH10_4F_R1C_MANIFEST.json').read_text(encoding='utf-8'))
    sources={
        'International': ROOT/'batch10_4c/manuscripts/International_v0.13-EVIDENCE-SATURATED.docx',
        'Brazil': ROOT/'batch10_4c/manuscripts/Brazil_v0.13-EVIDENCE-SATURATED.docx',
    }
    outputs={
        'International': OUT/'manuscripts/International_v0.14-RECONCILED.docx',
        'Brazil': OUT/'manuscripts/Brazil_v0.14-RECONCILED.docx',
    }
    for key, source in sources.items():
        assert source.exists() and outputs[key].exists()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == m['source_v013_sha256'][key]
