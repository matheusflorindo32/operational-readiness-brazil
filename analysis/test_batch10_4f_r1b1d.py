import csv,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'batch10_4f_r1b1d'
def rd(name):
 with (O/name).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_final_packet_completeness_and_depths():
 m=json.loads((O/'BATCH10_4F_R1B1D_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='EVIDENCE_PACKET_CONSOLIDATION_PASS'
 assert m['reference_packets_finalized']=='16/16'
 assert m['source_insufficient']=='6/16'
 p=rd('FINAL_16_REFERENCE_EVIDENCE_PACKETS.csv');assert len(p)==16
 assert {x['Source_Depth'] for x in p}=={'FULL_TEXT_RESULT_READY','GOVERNMENT_GUIDANCE_READY','ABSTRACT_RESULT_READY','SOURCE_INSUFFICIENT'}
 assert all(x['Packet_Status'].startswith('PACKET_COMPLETE_') for x in p)
def test_id_locator_guidance_identity_and_null_controls():
 r=rd('FINAL_RESULT_LEVEL_EVIDENCE_LEDGER.csv');assert len(r)==15
 assert len({x['Result_ID'] for x in r})==15 and all(x['Source_Locator'] and x['PDF_Page'] for x in r)
 g=rd('FINAL_GUIDANCE_LEDGER.csv');assert len(g)==2 and len({x['Guidance_ID'] for x in g})==2
 assert not {x['Guidance_ID'] for x in g}&{x['Result_ID'] for x in r}
 i=rd('EV1474_IDENTITY_FINAL.csv')[0];assert i['Identity_Status']=='EV1474_PUBLISHER_IDENTITY_PASS';assert i['Legacy_PMCID_Status']=='REJECTED_NOT_THIS_ARTICLE'
 n=rd('FINAL_NULL_RESULT_LEDGER.csv');assert len(n)>=4
def test_crosswalk_availability_only_and_no_same_cohort_inflation():
 c=rd('SENTENCE_RESULT_CANDIDATE_CROSSWALK_V4.csv');assert len(c)==168
 assert all(x['Sentence_Support_Adjudication']=='NOT_PERFORMED_IN_R1B1D' for x in c)
 assert set(x['Candidate_Result_Availability'] for x in c)<={'RESULTS_AVAILABLE','GUIDANCE_AVAILABLE','ABSTRACT_RESULT_AVAILABLE','NO_RESULT_LEVEL_SOURCE'}
 co=rd('FINAL_COHORT_RELATIONSHIP.csv'); rel={x['Evidence_ID']:x for x in co}
 assert rel['EV-1473']['Independent_Cohort_Count']=='1' and rel['EV-1474']['Independent_Cohort_Count']=='1'
 assert len(rd('CITATION_CHANGE_SOURCE_COVERAGE_FINAL.csv'))==147
 assert len(rd('NARROWING_SOURCE_COVERAGE_FINAL.csv'))==21
