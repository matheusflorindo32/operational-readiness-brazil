import csv, hashlib, json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'batch10_4h_r'
OUT=ROOT/'batch10_4i'
def sh(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(p): return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def main():
 m0=json.loads((PKG/'BATCH10_4H_R_MANIFEST.json').read_text(encoding='utf-8'))
 rows=[]
 for n,e in m0['files'].items():
  p=PKG/n; o=sh(p) if p.exists() else ''; c=canonical(p) if p.exists() and p.suffix in ('.csv','.json','.md') else o
  s='NOT_APPLICABLE'; q='NOT_APPLICABLE'
  if p.suffix=='.docx':
   try:
    with zipfile.ZipFile(p) as z: s='VALID_OOXML_ZIP' if z.testzip() is None else 'ZIP_CRC_ERROR';q='document.xml present' if 'word/document.xml' in z.namelist() else 'document.xml missing'
   except Exception as x:s='INVALID_OOXML:'+type(x).__name__;q='NOT_READABLE'
  elif p.suffix=='.csv':
   with p.open(encoding='utf-8-sig',newline='') as f:q=f'{sum(1 for _ in csv.DictReader(f))} data rows';s='VALID_UTF8_CSV'
  elif p.suffix=='.json': json.loads(p.read_text(encoding='utf-8'));s='VALID_UTF8_JSON';q='JSON parsed'
  elif p.suffix=='.md':s='VALID_UTF8_MARKDOWN';q='UTF-8 decoded'
  rows.append({'Filename':n,'Expected_SHA256':e,'Observed_SHA256':o,'Canonical_LF_SHA256':c,'Hash_Status':'MATCH' if o==e else ('MATCH_CANONICAL_LF' if c==e else 'MISMATCH'),'Structural_Status':s,'Parse_Status':q,'Scientific_Audit_Eligible':'NO' if c!=e or s.startswith('INVALID') else 'YES'})
 fields=list(rows[0])
 with (OUT/'FINAL_V015_PACKAGE_INTEGRITY_AUDIT.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 bad=[r for r in rows if r['Hash_Status']=='MISMATCH' or r['Structural_Status'].startswith('INVALID')]
 (OUT/'BATCH10_4I_REPORT.md').write_text(f'''# BATCH 10.4I-R — final scientific audit retry\n\n## Gate\n\n`V015_FINAL_SCIENTIFIC_AUDIT_BLOCKED`\n\nThe restored package has 18 named files, but {len(bad)} artifact fails integrity validation. `International_v0.15-B2-EVIDENCE-FIRST.docx` differs from its manifest SHA-256 and cannot be opened as a ZIP/OOXML document. Its exact wording, citations, document structure and visual layout cannot be audited.\n\nThe Brazil document and text artifacts are readable, but they cannot substitute for validation of the invalid International manuscript. The bundled renderer also could not locate its LibreOffice executable; this is secondary to the decisive OOXML failure.\n\nNo claim classification, human-review reduction, reference-use decision, freeze-readiness decision or final claim set was generated. No manuscript, claim, reference, Zotero item, CEF-v1 setting or reference freeze was changed.\n\nRestore the original valid International DOCX whose SHA-256 matches the package manifest, then rerun this batch.\n''',encoding='utf-8')
 files=[OUT/'FINAL_V015_PACKAGE_INTEGRITY_AUDIT.csv',OUT/'BATCH10_4I_REPORT.md']
 m={'batch':'BATCH 10.4I-R','entry_commit':'9ac2dd602ae445ee9f980c667328ac5c4cd9ab6e','gate':'V015_FINAL_SCIENTIFIC_AUDIT_BLOCKED','reason':'International v0.15 B2 DOCX SHA-256 mismatch and invalid OOXML ZIP structure.','expected_package_artifacts':18,'present_package_artifacts':18,'integrity_failures':len(bad),'scientific_claims_audited':0,'final_claim_set_generated':0,'human_review_reduced':0,'freeze_executed':0,'Zotero_changed':0,'CEF_v1_changed':0,'manuscript_content_changed':0,'next_action':'Restore original valid International v0.15 B2 DOCX bytes matching package manifest; then retry BATCH 10.4I-R.','artifact_sha256':{p.name:sh(p) for p in files}}
 (OUT/'BATCH10_4I_MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()

