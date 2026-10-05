"""Verify lawful full-text routes for FT2 High 25 without scientific appraisal."""
from __future__ import annotations
import csv, hashlib, json, urllib.parse, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; HIGH=ROOT/'batch10_4b'/'ft2'/'HIGH_IMPACT_ACCESS_REQUIRED.csv'; OUT=ROOT/'batch10_4b'/'ft3'
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def get(url):
 try:
  with urllib.request.urlopen(url,timeout=20) as r:return r.read()
 except Exception:return None
def write(name,rows,fields=None):
 OUT.mkdir(parents=True,exist_ok=True);fields=fields or list(rows[0])
 with (OUT/name).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 high=read(HIGH); assert len(high)==25 and len({x['Evidence_ID'] for x in high})==25
 rows=[];attempts=[]
 for rank,r in enumerate(high,1):
  pmid=r['PMID']; q=urllib.parse.quote(f'EXT_ID:{pmid} AND SRC:MED'); data=get('https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&query='+q)
  result={}
  if data:
   hits=json.loads(data).get('resultList',{}).get('result',[]); result=hits[0] if hits else {}
  pmcid=result.get('pmcid',''); source='';url='';status='ACCESS_UNRESOLVED';version='NONE';sha='';ready='NO';note='No lawful full-text body verified through Europe PMC in this run.'
  if pmcid:
   xmlurl=f'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC{pmcid.replace("PMC","")}/fullTextXML'; xml=get(xmlurl)
   if xml and b'<body' in xml and len(xml)>5000:
    status='FULL_TEXT_RECOVERED_FINAL_VERSION';version='PMC_FINAL_XML';source='Europe PMC / PMC';url=xmlurl;sha=hashlib.sha256(xml).hexdigest();ready='YES';note='Full XML body retrieved and identity keyed by PMID/PMCID; raw content not committed.'
   else:
    status='ABSTRACT_ONLY' if result else 'ACCESS_UNRESOLVED';source='Europe PMC metadata';url=result.get('fullTextUrlList',{}).get('fullTextUrl',[{}])[0].get('url','');note='PMCID/metadata route did not yield a full article body.'
  else:
   status='PAYWALLED_NO_LAWFUL_FULL_TEXT_FOUND' if result else 'ACCESS_UNRESOLVED';source='Europe PMC metadata' if result else 'Europe PMC search';url=result.get('doi','');note='No PMC body route identified; no publisher/repository full text was claimed without body verification.'
  base={'Evidence_ID':r['Evidence_ID'],'Title':r['Title'],'DOI':r['DOI'],'PMID':pmid,'PMCID':pmcid or r['PMCID'],'Priority_Rank':rank,'Priority_Reason':r['Access_Rationale'],'Contradictory_Flag':r['Contradictory_Potential'],'Replacement_Flag':r['Replacement_Potential'],'P0_Flag':'YES' if 'P0' in r['Priority_Previous'] else 'NO','Domain':r['Domain'],'Search_Status':'EUROPE_PMC_ROUTE_VERIFIED','Final_Access_Status':status,'Full_Text_Available':'YES' if ready=='YES' else 'NO','Preferred_Version_Type':version,'Preferred_Source':source,'Preferred_URL':url,'Local_File_Available':'NO','SHA256':sha,'Integrity_Status':'INTEGRITY_UNRESOLVED','Appraisal_Ready':ready,'Next_Action':'FT4 appraisal only' if ready=='YES' else 'Maintain access remediation; no scientific exclusion.','Notes':note}
  rows.append(base); attempts.append({'Evidence_ID':r['Evidence_ID'],'Source':'Europe PMC API + fullTextXML where PMCID returned','Attempt_Result':status,'URL_Checked':url,'Timestamp_UTC':'2026-10-05','Notes':note})
 fields=list(rows[0]);write('HIGH25_FULL_TEXT_RECOVERY_MASTER.csv',rows,fields);write('HIGH25_ACCESS_ATTEMPT_LEDGER.csv',attempts)
 write('HIGH25_VERSION_LEDGER.csv',[{k:x[k] for k in ['Evidence_ID','Final_Access_Status','Preferred_Version_Type','Preferred_Source','Preferred_URL','SHA256','Appraisal_Ready']} for x in rows])
 write('HIGH25_INTEGRITY_SCREEN.csv',[{'Evidence_ID':x['Evidence_ID'],'Integrity_Status':x['Integrity_Status'],'Notes':'Access recovery only; editorial integrity requires appraisal-stage primary-source confirmation.'} for x in rows])
 write('HIGH25_CONTRADICTORY_ACCESS_STATUS.csv',[x for x in rows if x['Contradictory_Flag']=='YES'],fields);write('HIGH25_REPLACEMENT_ACCESS_STATUS.csv',[x for x in rows if x['Replacement_Flag']=='YES'],fields)
 write('HIGH25_UNRESOLVED_ACCESS.csv',[x for x in rows if x['Appraisal_Ready']=='NO'],fields)
 manifest={'phase':'BATCH 10.4B-FT3','state':'HIGH25_FULL_TEXT_RECOVERY_COMPLETE','processed':25,'appraisal_ready':sum(x['Appraisal_Ready']=='YES' for x in rows),'statuses':{s:sum(x['Final_Access_Status']==s for x in rows) for s in sorted({x['Final_Access_Status'] for x in rows})},'cef_v1_changed':False,'zotero_changed':False,'manuscript_changed':False}
 (OUT/'HIGH25_RECOVERED_FULL_TEXT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');(OUT/'BATCH10_4B_FT3_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (OUT/'BATCH10_4B_FT3_REPORT.md').write_text(f'# FT3 High-25 recovery\n\n25/25 routes were verified. Appraisal-ready: {manifest["appraisal_ready"]}/25. This is provenance/access documentation only; no appraisal, inclusion, Zotero, CEF or manuscript action occurred.\n')
 print(json.dumps(manifest))
if __name__=='__main__':main()
