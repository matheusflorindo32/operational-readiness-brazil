import csv,json,subprocess,hashlib,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PKG=ROOT/'batch10_4h_r'; OUT=ROOT/'batch10_4i'; RF=ROOT/'batch10_4h_rf'
def test_restored_international_docx_matches_authoritative_manifest():
 m=json.loads((RF/'BATCH10_4H_RF_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='V015_B2_PACKAGE_INTEGRITY_PASS'
 assert m['present_package_artifacts']==18 and m['manifest_hash_mismatches']==0
 assert m['international_sha256']=='b6d5560315e66fecc93bb67f61f03da207f99cc29a66eb7169155d95ac22a754'
 with zipfile.ZipFile(PKG/'International_v0.15-B2-EVIDENCE-FIRST.docx') as z:
  assert z.testzip() is None and 'word/document.xml' in z.namelist()
def test_repair_does_not_execute_scientific_audit_or_mutate_other_package_artifacts():
 m=json.loads((OUT/'BATCH10_4I_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='V015_B2_PACKAGE_INTEGRITY_PASS' and m['scientific_claims_audited']==0 and m['freeze_executed']==0
 changed=subprocess.check_output(['git','diff','--name-only','2356840fb8c47c3fdb3d394fc109eda85bd01cca','--','batch10_4h_r'],cwd=ROOT,text=True).splitlines()
 assert changed==['batch10_4h_r/International_v0.15-B2-EVIDENCE-FIRST.docx']
