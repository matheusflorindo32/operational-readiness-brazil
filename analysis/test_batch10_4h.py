import csv,json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4h'
def rows(name):
 with (OUT/name).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_v015_claim_chains_are_complete_and_cover_all_approved_claims():
 matrix=rows('V015_CLAIM_CITATION_MATRIX.csv')
 ids={r['Reconstruction_Claim_ID'] for r in matrix}
 assert len(matrix)==12 and len(ids)==9
 assert all(r['Result_ID'] and r['Source_Locator'] and r['Evidence_ID'] and r['Citation'] for r in matrix)
def test_v015_null_overlap_and_controls_are_preserved():
 assert len(rows('V015_NULL_RESULT_AUDIT.csv'))==5
 overlap=rows('V015_COHORT_OVERLAP_AUDIT.csv')[0]
 assert overlap['Independent_Cohort_Count']=='1'
 m=json.loads((OUT/'BATCH10_4H_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='V015_RECONSTRUCTION_INSUFFICIENT'
 for k in ['empirical_claims_without_result_id','result_ids_without_locator','blocked_evidence_support','source_insufficient_evidence_promoted','rejected_pmcid_reused','cohort_double_counting','null_suppression','causal_inflation','framework_validation_inflation','unsupported_national_generalization','CEF_v1_changes','Zotero_changes']:
  assert m[k]==0
def test_v015_docx_packages_and_protected_language_are_valid():
 for name in ['International_v0.15-EVIDENCE-FIRST.docx','Brazil_v0.15-EVIDENCE-FIRST.docx']:
  p=OUT/name
  with ZipFile(p) as z:assert z.testzip() is None
  with ZipFile(p) as z:
   xml=z.read('word/document.xml')
  text=' '.join(t.text or '' for t in ET.fromstring(xml).iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
  assert 'PROPOSED SYNTHESIS FRAMEWORK - NOT YET VALIDATED' in text
  for bad in ['caffeine solves sleep loss','caffeine restores readiness','caffeine replaces sleep','validated readiness score','national prevalence claim']:
   assert bad not in text.lower()
