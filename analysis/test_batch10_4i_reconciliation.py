import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4i'
def test_v015_audit_stops_when_authorities_are_absent():
 m=json.loads((OUT/'BATCH10_4I_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='V015_FINAL_SCIENTIFIC_AUDIT_BLOCKED'
 assert m['batch10_4h_r_local_exists'] is False
 assert m['batch10_4h_r_tracked_file_count']==0
 assert m['authorities_present']==0
 assert m['scientific_claims_audited']==0
 assert m['reference_freeze_executed']==0
 assert m['Zotero_changed']==m['CEF_v1_changed']==m['v015_content_changed']==0
