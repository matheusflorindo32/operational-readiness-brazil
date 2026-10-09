import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4i'
def test_v015_scientific_audit_blocks_on_invalid_international_docx():
 m=json.loads((OUT/'BATCH10_4I_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='V015_FINAL_SCIENTIFIC_AUDIT_BLOCKED'
 assert m['expected_package_artifacts']==m['present_package_artifacts']==18
 assert m['integrity_failures']==1 and m['scientific_claims_audited']==0
 assert m['freeze_executed']==m['Zotero_changed']==m['CEF_v1_changed']==m['manuscript_content_changed']==0
 with (OUT/'FINAL_V015_PACKAGE_INTEGRITY_AUDIT.csv').open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f))
 bad=[x for x in r if x['Hash_Status']=='MISMATCH']
 assert len(bad)==1 and bad[0]['Filename']=='International_v0.15-B2-EVIDENCE-FIRST.docx'
 assert bad[0]['Structural_Status'].startswith('INVALID_OOXML')
