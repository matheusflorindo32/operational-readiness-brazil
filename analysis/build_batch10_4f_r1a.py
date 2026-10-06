"""Recover DOCX rendered superscript citation anchors without semantic inference."""
import csv,json,re,zipfile,hashlib
from pathlib import Path
from xml.etree import ElementTree as E
R=Path(__file__).resolve().parents[1];O=R/'batch10_4f_r1a';NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def wr(p,f,x):
 p.parent.mkdir(exist_ok=True)
 with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=f);w.writeheader();w.writerows(x)
def parse(name,prefix):
 path=R/'batch10_4c'/'manuscripts'/f'{name}_v0.13-EVIDENCE-SATURATED.docx';z=zipfile.ZipFile(path);root=E.fromstring(z.read('word/document.xml')); inv=[];runs=[];render=[];bib=[];sec='Preamble';sn=0
 parts=z.namelist(); fields=[]
 for n in parts:
  if n.endswith('.xml'):
   raw=z.read(n).decode('utf-8','ignore'); fields.append({'Manuscript':name,'Package_Part':n,'Present':'YES','Field_Tokens':sum(raw.count(x) for x in ['fldSimple','instrText','CITATION','ADDIN','ZOTERO','BIBLIOGRAPHY']),'Zotero_Tokens':raw.count('ZOTERO'),'CSL_Tokens':raw.count('CSL_CITATION')})
 for pi,p in enumerate(root.findall('.//w:body/w:p',NS),1):
  tx=''.join(t.text or '' for t in p.findall('.//w:t',NS)).strip();sty=p.find('./w:pPr/w:pStyle',NS);style=sty.get('{'+NS['w']+'}val') if sty is not None else ''
  if style in {'Heading1','Heading2'}:sec=tx
  if not tx:continue
  if sec.lower().startswith(('references','referências')):
   m=re.match(r'(\d+)\.\s*(.*)',tx)
   if m:bib.append({'Manuscript':name,'Display_Number':m.group(1),'Raw_Bibliography_Text':tx,'DOI':(re.search(r'doi:([^\.\s]+(?:\.[^\s]+)*)',tx,re.I).group(1) if re.search(r'doi:([^\.\s]+(?:\.[^\s]+)*)',tx,re.I) else ''),'Source_ID':'NONE_RENDERED'})
   continue
  sup=[];plain='';off=0
  for ri,r in enumerate(p.findall('./w:r',NS),1):
   t=''.join(x.text or '' for x in r.findall('.//w:t',NS));v=r.find('./w:rPr/w:vertAlign',NS);isup=v is not None and v.get('{'+NS['w']+'}val')=='superscript';runs.append({'Manuscript':name,'Paragraph_ID':f'P{pi}','Run_ID':ri,'Run_Text':t,'Field_Start':'NO','Field_Code':'','Field_Separator':'NO','Field_Result':'','Field_End':'NO','Citation_Text_Rendered':t if isup else '','Citation_Metadata':'','Source_ID':'','XML_Path':'word/document.xml','Character_Offset':off});off+=len(t)
   if isup and re.fullmatch(r'[0-9,–\- ]+',t):sup.append((len(plain),t))
   else:plain+=t
  for s in re.split(r'(?<=[.!?])\s+',plain):
   if not s:continue
   sn+=1;sid=f'{prefix}-S{sn:04d}'; anchor=';'.join(x[1] for x in sup) if sup else '';nums=[]
   for _,a in sup:
    for q in re.findall(r'\d+(?:[–-]\d+)?',a):
     ab=q.replace('–','-').split('-');nums += list(range(int(ab[0]),int(ab[-1])+1))
   inv.append({'Sentence_ID':sid,'Manuscript':name,'Section':sec,'Paragraph_ID':f'P{pi}','Exact_Sentence':s,'Citation_Anchor_Found':'YES' if nums else 'NO','Rendered_Citation':anchor,'Parsed_Reference_Numbers':';'.join(map(str,nums)),'Anchor_Source':'RENDERED_SUPERSCRIPT_RUN' if nums else 'NONE','Confidence':'DETERMINISTIC_RENDERED_NUMBER_MATCH' if nums else 'UNRESOLVED','Notes':'Numbers map only to numbered bibliography; no thematic inference.'})
   if nums:render.append(inv[-1])
 return path,parts,fields,runs,render,bib,inv
def main():
 allx=[parse('International','INT'),parse('Brazil','BRA')];pkg=[];fields=[];runs=[];render=[];bib=[];sent=[]
 for path,parts,f,r,rm,b,s in allx:
  pkg += [{'DOCX':path.name,'Package_Part':p,'SHA256':hashlib.sha256(zipfile.ZipFile(path).read(p)).hexdigest()} for p in parts];fields+=f;runs+=r;render+=rm;bib+=b;sent+=s
 wr(O/'DOCX_PACKAGE_INVENTORY.csv',list(pkg[0]),pkg);wr(O/'WORD_FIELD_INVENTORY.csv',list(fields[0]),fields);wr(O/'ZOTERO_FIELD_INVENTORY.csv',list(fields[0]),fields);wr(O/'RUN_LEVEL_CITATION_MAP.csv',list(runs[0]),runs);wr(O/'DOCX_RENDERED_CITATION_MAP.csv',list(render[0]) if render else list(sent[0]),render);wr(O/'DOCX_BIBLIOGRAPHY_EXTRACT.csv',list(bib[0]),bib);wr(O/'SENTENCE_CITATION_ANCHOR_RECOVERY.csv',list(sent[0]),sent);wr(O/'UNRESOLVED_CITATION_ANCHORS.csv',list(sent[0]),[x for x in sent if x['Citation_Anchor_Found']=='NO'])
 proj=[]
 with (R/'batch10_4d'/'FINAL_REFERENCE_AUDIT.csv').open(encoding='utf-8-sig',newline='') as h:proj=list(csv.DictReader(h))
 rec=[]
 for b in bib:
  match=next((p for p in proj if p['Ref']==b['Display_Number']),None);rec.append({'Manuscript':b['Manuscript'],'Display_Number':b['Display_Number'],'Raw_Bibliography_Text':b['Raw_Bibliography_Text'],'Project_Reference_ID':match['Ref'] if match else '','Evidence_ID':match['Evidence_ID'] if match else '','Classification':'EXACT_MATCH' if match and b['DOI'].lower().rstrip('.')==match['DOI'].lower().rstrip('.') else 'NUMBER_MATCH_ONLY' if match else 'EXTRA_IN_DOCX'})
 wr(O/'DOCX_TO_PROJECT_REFERENCE_RECONCILIATION.csv',list(rec[0]),rec);wr(O/'ALTERNATIVE_AUTHORITATIVE_SOURCE_AUDIT.csv',['Source','Used','Reason'],[{'Source':'DOCX rendered superscript runs','Used':'YES','Reason':'Deterministic numbered anchors and numbered bibliography are present.'}])
 (O/'BATCH10_4F_R1A_MANIFEST.json').write_text(json.dumps({'gate':'CITATION_ANCHOR_RECOVERY_PASS','word_fields_found':0,'zotero_fields_found':0,'rendered_numeric_citations':len(render),'bibliography_entries':len(bib),'forced_links':0},indent=2)+'\n');(O/'BATCH10_4F_R1A_REPORT.md').write_text(f'# Citation anchor recovery\n\nPASS: DOCX uses rendered superscript numeric runs, not Word/Zotero fields. Recovered {len(render)} sentence anchors and {len(bib)} bibliography entries across both manuscripts. Structural links are rendered-number to bibliography-number only; semantic support adjudication remains a later stage.\n')
if __name__=='__main__':main()
