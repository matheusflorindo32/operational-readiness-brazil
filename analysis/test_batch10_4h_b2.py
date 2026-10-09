import csv, hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4h_b2'
def rows(n):
 with (OUT/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def test_scope_pruning_and_required_outputs():
 req=['FINAL_DOMAIN_SCOPE_MATRIX.csv','FINAL_B2_CLAIM_LIBRARY.csv','FINAL_B2_CLAIM_RESULT_MATRIX.csv','FINAL_B2_EVIDENCE_DENSITY.csv','FINAL_B2_WORKING_REFERENCE_SET.csv','FINAL_B2_INDEPENDENT_COHORT_COUNT.csv','EV1467_CLAIM_INTEGRATION.csv','REMOVED_DOMAIN_JUSTIFICATION.csv','INTERNATIONAL_B2_BLUEPRINT.md','BRAZIL_B2_BLUEPRINT.md','B2_VS_C_REASSESSMENT.csv','B2_MANUSCRIPT_VIABILITY.csv','B2_HUMAN_REVIEW_QUEUE.csv','B2_FCR_CANDIDATES.csv','BATCH10_4H_B2_MANIFEST.json','BATCH10_4H_B2_REPORT.md']
 assert all((OUT/x).exists() for x in req)
 domains=rows('FINAL_DOMAIN_SCOPE_MATRIX.csv')
 assert {x['Domain'] for x in domains if x['Core_Status']=='REMOVED_FROM_CORE_SCOPE'}=={'Nutrition / supplementation','Physical fitness / academy readiness','Hydration / heat'}
def test_claim_chain_and_contradictory_guards():
 c=rows('FINAL_B2_CLAIM_LIBRARY.csv'); m=json.loads((OUT/'BATCH10_4H_B2_MANIFEST.json').read_text(encoding='utf-8'))
 assert len(c)==14 and all(x['Evidence_ID'] and x['Result_ID'] and x['Locator'] for x in c)
 assert all(x['B2_Disposition']=='REMOVE_FROM_MANUSCRIPT' for x in c if x['Evidence_ID'] in {'EV-0426','EV-0521','EV-0204','EV-0667'})
 for k in ['unresolved_domains_promoted_to_core','hydration_claims_without_result_id','nutrition_claims_relying_on_EV0140','fitness_core_claims_relying_on_EV0052_or_EV1066','source_insufficient_evidence_promoted','blocked_evidence_support','cohort_double_counting','null_suppression','framework_validation_inflation','CEF_v1_unauthorized_change','Zotero_changed','v015_changed']:
  assert m[k]==0
def test_manuscripts_unchanged():
 for p in ['batch10_4h/International_v0.15-EVIDENCE-FIRST.docx','batch10_4h/Brazil_v0.15-EVIDENCE-FIRST.docx']:
  before=subprocess.check_output(['git','show',f'HEAD:{p}'],cwd=ROOT)
  assert hashlib.sha256((ROOT/p).read_bytes()).digest()==hashlib.sha256(before).digest()
