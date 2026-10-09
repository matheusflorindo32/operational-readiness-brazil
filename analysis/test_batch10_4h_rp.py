import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4h_rp'
def test_restoration_block_is_file_by_file_and_nonfabricated():
 m=json.loads((OUT/'BATCH10_4H_R_RESTORATION_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='V015_B2_AUTHORITATIVE_PACKAGE_RESTORATION_BLOCKED'
 assert m['expected_artifacts']==18 and m['restored_artifacts']==0 and m['missing_artifacts']==18
 assert m['unauthorized_scientific_changes']==m['Zotero_changes']==m['CEF_v1_changes']==m['v015_scientific_changes']==0
 with (OUT/'BATCH10_4H_R_RESTORATION_LEDGER.csv').open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f))
 assert len(r)==18
 assert all(x['Restoration_Status']=='NOT_RESTORED' and not x['SHA256'] for x in r)
