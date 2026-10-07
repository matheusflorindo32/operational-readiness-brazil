import csv, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]; O=R/'batch10_4f_r1b1c'
def rd(n):
 with (O/n).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_r1b1c_gate_and_identity():
 m=json.loads((O/'BATCH10_4F_R1B1C_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='VERIFIED_SOURCE_RESULT_EXTRACTION_PASS'
 assert m['full_texts_extracted_and_localized']==5
 assert m['sentence_re_adjudication']==0 and m['forced_semantic_links']==0
 ident=rd('EV1474_PUBLISHER_IDENTITY_VALIDATION.csv')[0]
 assert ident['Identity_Status']=='EV1474_PUBLISHER_IDENTITY_PASS'
 assert ident['Legacy_PMCID_Status']=='REJECTED_NOT_THIS_ARTICLE'
def test_r1b1c_boundaries_and_guidance():
 rows=rd('NEW_RESULT_LEVEL_EVIDENCE_LEDGER.csv')
 assert {x['Evidence_ID'] for x in rows}>={'EV-1474','EV-1475','EV-1476','EV-1479','EV-1482'}
 assert all(x['Source_Locator'] and x['PDF_Page'] for x in rows)
 assert all(x['Prohibited_Inference'] for x in rows)
 g=rd('EV1477_GUIDANCE_EXTRACTION.csv')
 assert len(g)==2 and all(x['Empirical_Result']=='NONE' for x in g)
def test_r1b1c_no_sentence_disposition_mutation_and_insufficiency_isolated():
 cross=rd('SENTENCE_RESULT_CANDIDATE_CROSSWALK_V3.csv')
 assert cross and all(x['Adjudication_Status']=='UNCHANGED; NOT PERFORMED IN R1B1C' for x in cross)
 insuff=rd('SOURCE_INSUFFICIENT_FINAL_FOR_R1B1C.csv')
 assert len(insuff)==6
