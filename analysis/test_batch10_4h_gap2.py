import csv, hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4h_gap2'
def rows(n):
 with (OUT/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def test_required_outputs_and_target_counts():
 required=['GAP2_TARGET_INVENTORY.csv','CONTRADICTORY_FULLTEXT_RECOVERY.csv','EV0052_ADJUDICATION.csv','EV0140_ADJUDICATION.csv','EV1066_ADJUDICATION.csv','BRAZIL_TARGETED_CANDIDATE_SCREEN.csv','HYDRATION_HEAT_TARGETED_SCREEN.csv','NEW_RESULT_LEVEL_EXTRACTION.csv','NEW_RESULT_SOURCE_LOCATORS.csv','NEW_BOUNDED_CLAIMS.csv','NEW_COHORT_OVERLAP_AUDIT.csv','GAP_STATUS_FINAL.csv','FCR_CANDIDATES.csv','UPDATED_RECONSTRUCTION_GAP_MATRIX.csv','BATCH10_4H_GAP2_MANIFEST.json','BATCH10_4H_GAP2_REPORT.md']
 assert all((OUT/n).exists() for n in required)
 assert len(rows('CONTRADICTORY_FULLTEXT_RECOVERY.csv'))==3
 assert len(rows('GAP_STATUS_FINAL.csv'))==4
def test_fail_closed_and_bounded_claim_chain():
 m=json.loads((OUT/'BATCH10_4H_GAP2_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='TARGETED_GAP_CLOSURE_INSUFFICIENT'
 assert m['contradictory_full_texts_recovered']==0
 assert m['contradictory_records_adjudicated']==0
 for k in ['forced_semantic_links','blocked_evidence_used','source_insufficient_evidence_promoted','cohort_double_counting','rejected_pmcid_reused','CEF_v1_silently_changed','Zotero_changed','v015_changed']:
  assert m[k]==0
 claims=rows('NEW_BOUNDED_CLAIMS.csv'); results=rows('NEW_RESULT_LEVEL_EXTRACTION.csv'); loc=rows('NEW_RESULT_SOURCE_LOCATORS.csv')
 assert len(claims)==len(results)==len(loc)==1
 assert claims[0]['Evidence_ID']==results[0]['Evidence_ID']==loc[0]['Evidence_ID']
 assert claims[0]['Result_ID']==results[0]['Result_ID']==loc[0]['Result_ID']
 assert claims[0]['Claim_Ready']=='NO' and claims[0]['Final_Reference_Promotion']=='NO'
def test_v015_unchanged_from_head():
 for p in ['batch10_4h/International_v0.15-EVIDENCE-FIRST.docx','batch10_4h/Brazil_v0.15-EVIDENCE-FIRST.docx']:
  expected=subprocess.check_output(['git','show',f'HEAD:{p}'],cwd=ROOT)
  assert hashlib.sha256((ROOT/p).read_bytes()).digest()==hashlib.sha256(expected).digest()
