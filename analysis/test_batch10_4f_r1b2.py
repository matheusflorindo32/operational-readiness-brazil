import csv,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'batch10_4f_r1b2'
def rd(n):
 with (O/n).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_r1b2_all_sentences_have_final_disposition_and_no_forced_links():
 m=json.loads((O/'BATCH10_4F_R1B2_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='SENTENCE_SUPPORT_READJUDICATION_PASS' and m['scientific_sentences_readjudicated']=='168/168'
 assert m['forced_semantic_links']==m['blocked_evidence_used']==m['rejected_pmcid_reused']==0
 r=rd('FINAL_SENTENCE_SUPPORT_READJUDICATION.csv');assert len(r)==168
 assert all(x['Final_Disposition'] and x['Individual_Support_Fit'] for x in r)
def test_r1b2_source_and_null_guards():
 r=rd('FINAL_SENTENCE_SUPPORT_READJUDICATION.csv');by={x['Sentence_ID']:x for x in r}
 assert by['INT-S0135']['Final_Disposition']=='DELETE_REQUIRED'
 assert by['INT-S0140']['Individual_Support_Fit']=='DIRECT_SUPPORT'
 assert by['INT-S0121']['Final_Disposition']=='NARROWING_REQUIRED'
 assert 'EV-1475-R01' in by['INT-S0121']['Result_ID_s']
 assert not any('PMC3382270' in x['Source_Locator_s'] for x in r)
def test_r1b2_outputs_and_reference_aggregation():
 assert len(rd('FINAL_CITATION_CHANGE_ACTIONS.csv'))==0
 assert len(rd('FINAL_CITATION_REMOVAL_ACTIONS.csv'))==0
 assert len(rd('FINAL_REFERENCE_VALID_USE_AUDIT.csv'))==16
 assert len(rd('FINAL_PROTECTED_CLAIM_AUDIT.csv'))==168
