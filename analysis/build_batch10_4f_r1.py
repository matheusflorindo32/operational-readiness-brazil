"""Inventory v0.13 manuscript sentences without forcing FT8 links."""
import csv,json,re,zipfile
from pathlib import Path
from xml.etree import ElementTree as E
R=Path(__file__).resolve().parents[1];O=R/'batch10_4f_r1';NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def wr(p,f,x):
 p.parent.mkdir(exist_ok=True)
 with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=f);w.writeheader();w.writerows(x)
def doc(name,prefix):
 root=E.fromstring(zipfile.ZipFile(R/'batch10_4c'/'manuscripts'/f'{name}_v0.13-EVIDENCE-SATURATED.docx').read('word/document.xml'));sec='Preamble';out=[];n=0
 for pi,p in enumerate(root.findall('.//w:body/w:p',NS),1):
  text=''.join(t.text or '' for t in p.findall('.//w:t',NS)).strip();st=p.find('./w:pPr/w:pStyle',NS);style=st.get('{'+NS['w']+'}val') if st is not None else ''
  if style in {'Heading1','Heading2'}:sec=text
  if not text or sec.lower().startswith(('references','referências')):continue
  for s in re.split(r'(?<=[.!?])\s+',text):
   if not s:continue
   n+=1;low=s.lower();scientific=bool(re.search(r'\b(association|associated|correlat|increased|decreased|improv|supports|evidence|study|studies|cohort|trial|risk|effect|resultado|associa|correla|aument|reduz|estudo|evidência|coorte)\b',low))
   cat='SCIENTIFIC_CLAIM_REQUIRES_SUPPORT' if scientific else ('LIMITATION_STATEMENT' if 'limitation' in low or 'limita' in low else 'METHOD_STATEMENT' if sec.lower().startswith(('methods','método')) else 'FRAMEWORK_PROPOSAL' if 'framework' in low else 'NON_EVIDENTIARY_TEXT')
   out.append({'Sentence_ID':f'{prefix}-S{n:04d}','Manuscript':name,'Section':sec,'Paragraph_ID':f'P{pi}','Exact_Sentence':s,'Classification':cat,'Existing_Citation_Numbers':'NOT_DETERMINISTICALLY_EXTRACTABLE_FROM_V013_DOCX','Final_Sentence_Status':'PENDING_SENTENCE_LEVEL_CITATION_RECONCILIATION' if scientific else 'CLASSIFIED_NONACTIVE'})
 return out
def main():
 inv=doc('International','INT')+doc('Brazil','BRA');wr(O/'MANUSCRIPT_SENTENCE_INVENTORY.csv',list(inv[0]),inv);wr(O/'SCIENTIFIC_SENTENCE_CLASSIFICATION.csv',list(inv[0]),inv)
 sci=[x for x in inv if x['Classification']=='SCIENTIFIC_CLAIM_REQUIRES_SUPPORT'];wr(O/'UNSUPPORTED_SENTENCE_LEDGER.csv',list(sci[0]) if sci else list(inv[0]),sci)
 ft=[]
 with (R/'batch10_4e'/'HR001_UNLINKED_CLAIMS.csv').open(encoding='utf-8-sig',newline='') as h:
  for x in csv.DictReader(h):ft.append({'Claim_ID':x['Claim_ID'],'HR001_Status':x['Final_Status'] if 'Final_Status' in x else x.get('Disposition','UNLINKED_NARROWING_REQUIRED'),'Final_Disposition':'NOT_PRESENT_IN_MANUSCRIPT_NO_ACTION','Rationale':'FT8 ledger claim is not forced into manuscript text during manuscript-first reconciliation.'})
 wr(O/'FT8_CLAIM_FINAL_DISPOSITION.csv',list(ft[0]),ft);wr(O/'FT8_TO_MANUSCRIPT_CROSSWALK.csv',list(ft[0]),ft)
 report=f'''# Batch 10.4F-R1 sentence-level reconciliation\n\nSentence inventory created: {len(inv)} total; {len(sci)} heuristically identified scientific sentences require manual citation extraction. The v0.13 DOCX text layer does not expose deterministic citation-number anchors for those sentences. Existing reference-use counts cannot establish exact sentence support without forcing a link.\n\nGate: `MANUSCRIPT_SENTENCE_LEVEL_RECONCILIATION_BLOCKED`. Blocking resolution: extract/normalize citation anchors from the Word field/run structure or use an authoritative citation-marked source, then adjudicate every scientific sentence. FT8 claims are ledger candidates and retain non-forced dispositions. No freeze, manuscript, CEF-v1 or Zotero action occurred.\n''';(O/'BATCH10_4F_R1_REPORT.md').write_text(report,encoding='utf-8');(O/'BATCH10_4F_R1_MANIFEST.json').write_text(json.dumps({'gate':'MANUSCRIPT_SENTENCE_LEVEL_RECONCILIATION_BLOCKED','sentences':len(inv),'scientific_sentences_pending':len(sci),'forced_mappings':0,'freeze_executed':False},indent=2)+'\n')
if __name__=='__main__':main()
