import csv,json,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4h_gap'
def rows(n):
 with (OUT/n).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_gap_claims_have_complete_chains_and_are_not_promoted():
 claims=rows('GAP_CLOSURE_NEW_CLAIMS.csv')
 assert len(claims)==4
 assert all(r['Evidence_ID'] and r['Result_ID'] and r['Source_Locator'] for r in claims)
 assert all(r['Eligibility_for_Reconstruction']=='CONDITIONAL_PENDING_HUMAN_REVIEW' for r in claims)
def test_gap_controls_and_remaining_gaps_are_explicit():
 m=json.loads((OUT/'BATCH10_4H_GAP_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='TARGETED_GAP_CLOSURE_INSUFFICIENT'
 for k in ['new_final_references','new_claim_ready','blocked_evidence_support','source_insufficient_evidence_promoted','rejected_pmcid_reused','cohort_double_counting','null_suppression','CEF_v1_changes','Zotero_changes','v015_changes']:
  assert m[k]==0
 assert len(rows('GAP_CLOSURE_REMAINING_GAPS.csv'))==4
def test_v015_artifacts_are_unchanged_from_head():
 for path in ['batch10_4h/International_v0.15-EVIDENCE-FIRST.docx','batch10_4h/Brazil_v0.15-EVIDENCE-FIRST.docx']:
  expected=subprocess.check_output(['git','show',f'HEAD:{path}'],cwd=ROOT)
  assert hashlib.sha256((ROOT/path).read_bytes()).digest()==hashlib.sha256(expected).digest()
