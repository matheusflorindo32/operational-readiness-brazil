import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'batch10_4f_r1b'

def rows(name):
    with (OUT/name).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))

def test_sentence_adjudication_complete_and_conservative():
    data=rows('SENTENCE_SUPPORT_ADJUDICATION.csv')
    assert len(data)==168
    assert all(r['Final_Disposition'] for r in data)
    assert all(r['Support_Fit']=='INSUFFICIENT_SUPPORT' for r in data)
    assert all('DIRECT_SUPPORT' not in r['Support_Fit'] for r in data)

def test_no_forced_or_blocked_support_and_manifest():
    manifest=json.loads((OUT/'BATCH10_4F_R1B_MANIFEST.json').read_text(encoding='utf-8'))
    assert manifest['gate']=='SENTENCE_SUPPORT_ADJUDICATION_BLOCKED'
    assert manifest['forced_links']==0
    assert manifest['blocked_evidence_used_as_support']==0
    assert manifest['scientific_sentences_adjudicated']==168

def test_citation_links_are_structural_only():
    data=rows('SENTENCE_REFERENCE_FIT_MATRIX.csv')
    assert all(r['Forced_Link']=='NO' for r in data)
