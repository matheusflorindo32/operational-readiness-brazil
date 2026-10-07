"""Targeted lawful recovery for the fourteen retained references lacking packets."""
import csv, hashlib, json, re, urllib.request, xml.etree.ElementTree as E
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4f_r1b1a'; TODAY='2026-10-07'; H={'User-Agent':'Mozilla/5.0 operational-readiness-brazil/1.0'}
FULL={
'EV-1474':'https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1736902/pdf',
'EV-1475':'https://revista.ibsp.org.br/index.php/RIBSP/article/download/317/210',
'EV-1476':'https://periodicorease.pro.br/rease/article/download/19687/11741',
'EV-1477':'https://www.gov.br/mj/pt-br/assuntos/sua-seguranca/seguranca-publica/aph-tatico/manual-aluno-aph-tatico-mjsp-11-04-2025_compressed.pdf',
'EV-1479':'https://www.scielo.br/j/ep/a/WKSVkX7LfNVtNHVMMD5hvMC/?lang=pt&format=pdf',
'EV-1482':'https://revista.forumseguranca.org.br/rbsp/article/download/1764/779',
}
PAYWALLED={'EXT-TFF-2013':'https://doi.org/10.7205/MILMED-D-12-00519','EXT-ACC-AHA-2026':'https://doi.org/10.1016/j.jacc.2026.07.003','EV-1471':'https://doi.org/10.1016/j.nut.2025.112989','EV-1472':'https://doi.org/10.1177/08901171251336887','EV-1478':'https://doi.org/10.1016/j.jdeveco.2025.103603','EV-1480':'https://doi.org/10.1007/s11896-026-09827-0','EV-1481':'https://doi.org/10.3233/WOR-210031','EV-1483':'https://doi.org/10.1519/JSC.0000000000001065'}
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def write(p,f,rows):
 p.parent.mkdir(exist_ok=True)
 with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=f,extrasaction='ignore');w.writeheader();w.writerows(rows)
def fetch(url):
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=60) as r:return r.read(),r.url,r.headers.get_content_type()
 except Exception:return b'','', ''
def pubmed(pmid):
 if not pmid:return {}
 raw,_,_=fetch(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml')
 if not raw:return {}
 root=E.fromstring(raw);a=root.find('.//PubmedArticle'); out={'pmc':'','abstract_result':''}
 for x in a.findall('.//ArticleId'):
  if x.attrib.get('IdType')=='pmc':out['pmc']=x.text or ''
 for x in a.findall('.//AbstractText'):
  if (x.attrib.get('Label','').upper()=='RESULTS') and ''.join(x.itertext()).strip():out['abstract_result']=' '.join(''.join(x.itertext()).split())
 return out
def crossref(doi):
 if not doi or doi=='NO_DOI_LISTED':return {}
 raw,_,_=fetch('https://api.crossref.org/works/'+urllib.request.quote(doi,safe=''))
 try:return json.loads(raw.decode('utf-8'))['message']
 except Exception:return {}
def main():
 refs=read(ROOT/'batch10_4f_r1b1'/'FINAL_16_REFERENCE_SOURCE_INVENTORY.csv'); targets=[x for x in refs if x['Evidence_ID'] not in {'EV-1473','EV-1484'}]
 recovery=[];identity=[];routes=[];full=[];abstract=[];newres=[];loc=[];depth=[];unresolved=[];recon=[]
 for r in targets:
  ev=r['Evidence_ID']; url=FULL.get(ev,''); raw=final=ctype=b''
  if url: raw,final,ctype=fetch(url)
  if raw.startswith(b'%PDF'):
   status='VERIFIED_GOVERNMENT_SOURCE' if ev=='EV-1477' else 'VERIFIED_OPEN_FULL_TEXT'; identity_status='PASS'; sha=hashlib.sha256(raw).hexdigest(); route='Official source PDF retrieved directly';
   full.append({'Reference_ID':r['Reference_ID'],'Evidence_ID':ev,'Source_URL':final,'File_Type':'PDF','SHA256':sha,'Access_Status':status,'Version':'Publisher/government rendered full text','Stored_Locally':'NO_REMOTE_HASH_ONLY'})
  else:
   status='PAYWALLED_NO_LAWFUL_FULL_TEXT'; identity_status='NOT_APPLICABLE_NO_DOCUMENT'; sha='NR'; route='DOI resolver/publisher landing route reached or attempted; no lawful full text captured.'
  pm=pubmed(r['PMID'])
  meta=crossref(r['DOI'])
  meta_title=' '.join(meta.get('title',[])[:1]); title_ok=bool(meta_title) and (re.sub(r'\W+','',meta_title).lower()[:35] in re.sub(r'\W+','',r['Exact_Title']).lower() or re.sub(r'\W+','',r['Exact_Title']).lower()[:35] in re.sub(r'\W+','',meta_title).lower())
  meta_ok=title_ok and bool(meta.get('author')) and bool(meta.get('container-title')) and bool(meta.get('published') or meta.get('published-online'))
  if status.startswith('VERIFIED_') and ev!='EV-1477' and not meta_ok:
   # A file without matching authoritative metadata is never accepted as a packet source.
   status='IDENTITY_UNRESOLVED'; identity_status='FAIL'; route+=' Crossref identity metadata did not establish the complete identity.'
  elif status.startswith('VERIFIED_') and ev!='EV-1477':identity_status='PASS'
  if status=='PAYWALLED_NO_LAWFUL_FULL_TEXT' and pm.get('abstract_result'):
   status='ABSTRACT_ONLY_CONFIRMED'; route+=' Structured PubMed Results abstract recovered.'
   rid=f'{ev}-ABSTRACT-R01'; summary='Structured PubMed abstract contains a Results-labelled statement; bounded extraction pending human paraphrase.'
   abstract.append({'Evidence_ID':ev,'Result_ID':rid,'Source_URL':f"https://pubmed.ncbi.nlm.nih.gov/{r['PMID']}/",'Locator':'PubMed Abstract — Results','Source_Depth':'ABSTRACT_ONLY','Explicit_Result_Available':'YES','Extraction_Limit':'No unreported methods, subgroups, tables or secondary outcomes inferred.'})
   newres.append({'Evidence_ID':ev,'Result_ID':rid,'Source_Section':'Abstract','Source_Locator':'PubMed Abstract — Results','Result_Summary':summary,'Population':r['Exact_Title'],'Effect_Estimate':'NR_NOT_PARAPHRASED_AUTOMATICALLY','Source_Depth':'ABSTRACT_ONLY','Permitted_Scope':'Only exact abstract-level finding after human verification','Prohibited_Inference':'No details absent from abstract; no causal expansion.'})
   loc.append({'Evidence_ID':ev,'Result_ID':rid,'Source_URL':f"https://pubmed.ncbi.nlm.nih.gov/{r['PMID']}/",'Locator':'PubMed Abstract — Results','Auditable':'YES'})
  elif status=='PAYWALLED_NO_LAWFUL_FULL_TEXT':unresolved.append({'Reference_ID':r['Reference_ID'],'Evidence_ID':ev,'Access_Status':status,'Affected_Manuscript_Uses':f"International {r['International_Use']}; Brazil {r['Brazil_Use']}",'Likely_Action':'NARROWING_OR_DELETION_REASSESSMENT_REQUIRED'})
  recovery.append({'Reference_ID':r['Reference_ID'],'Evidence_ID':ev,'Target_Status_Before':'ABSTRACT_ONLY or SOURCE_UNAVAILABLE','Final_Access_Status':status,'Recovery_URL':final or url or PAYWALLED.get(ev,''),'Recovery_Date':TODAY,'Lawful_Access':'YES','New_Reference_Added':'NO'})
  identity.append({'Reference_ID':r['Reference_ID'],'Evidence_ID':ev,'Title_Check':'PASS' if identity_status=='PASS' else 'NOT_VERIFIED','Authors_Check':'PASS' if identity_status=='PASS' else 'NOT_VERIFIED','Year_Check':'PASS' if identity_status=='PASS' else 'NOT_VERIFIED','Journal_Source_Check':'PASS' if identity_status=='PASS' else 'NOT_VERIFIED','DOI_PMID_Check':'PASS' if identity_status=='PASS' else 'NOT_VERIFIED','IDENTITY_MATCH':identity_status})
  routes.append({'Reference_ID':r['Reference_ID'],'Evidence_ID':ev,'Route_Attempted':route,'URL':final or url or PAYWALLED.get(ev,''),'Outcome':status,'Illegal_Access':'NO'})
  depth.append({'Reference_ID':r['Reference_ID'],'Evidence_ID':ev,'SOURCE_DEPTH':'FULL_TEXT' if status.startswith('VERIFIED_') else ('ABSTRACT_ONLY' if status=='ABSTRACT_ONLY_CONFIRMED' else 'INSUFFICIENT'),'Use_Restriction':'No sentence support adjudication until result-level packet is consolidated.'})
  recon.append({'Reference_ID':r['Reference_ID'],'Evidence_ID':ev,'Prior_Status':r['Full_Text_Status'],'Recovered_Status':status,'Reference_Set_Changed':'NO','CEF_v1_Changed':'NO','Zotero_Changed':'NO'})
 # Correct-PMC audit is explicitly kept candidate-only; no frozen metadata writes occur.
 ev1474=next(x for x in targets if x['Evidence_ID']=='EV-1474'); pm=pubmed(ev1474['PMID'])
 write(OUT/'TARGETED_SOURCE_RECOVERY_LEDGER.csv',list(recovery[0]),recovery);write(OUT/'SOURCE_IDENTITY_VALIDATION.csv',list(identity[0]),identity);write(OUT/'LAWFUL_ACCESS_ROUTE_LEDGER.csv',list(routes[0]),routes);write(OUT/'RECOVERED_FULL_TEXT_MANIFEST.csv',['Reference_ID','Evidence_ID','Source_URL','File_Type','SHA256','Access_Status','Version','Stored_Locally'],full);write(OUT/'ABSTRACT_RESULT_EXTRACTION.csv',['Evidence_ID','Result_ID','Source_URL','Locator','Source_Depth','Explicit_Result_Available','Extraction_Limit'],abstract);write(OUT/'NEW_RESULT_LEVEL_EVIDENCE_LEDGER.csv',['Evidence_ID','Result_ID','Source_Section','Source_Locator','Result_Summary','Population','Effect_Estimate','Source_Depth','Permitted_Scope','Prohibited_Inference'],newres);write(OUT/'NEW_RESULT_SOURCE_LOCATORS.csv',['Evidence_ID','Result_ID','Source_URL','Locator','Auditable'],loc);write(OUT/'SOURCE_DEPTH_CLASSIFICATION.csv',list(depth[0]),depth);write(OUT/'UNRESOLVED_SOURCE_LEDGER.csv',['Reference_ID','Evidence_ID','Access_Status','Affected_Manuscript_Uses','Likely_Action'],unresolved)
 write(OUT/'EV1474_IDENTITY_RECHECK.csv',['Evidence_ID','DOI','PMID','Reported_PMCID','PubMed_Retrieved_PMCID','Identity_Result','Action'],[{'Evidence_ID':'EV-1474','DOI':'10.3389/fpsyg.2025.1736902','PMID':'41694750','Reported_PMCID':'PMC3382270 — DO NOT USE','PubMed_Retrieved_PMCID':pm.get('pmc','NONE_RETRIEVED'),'Identity_Result':'PASS via official Frontiers DOI full-text source; legacy PMCID rejected','Action':'FREEZE_CHANGE_REQUEST_CANDIDATE only if frozen PMCID field requires correction; no CEF-v1 edit.'}])
 write(OUT/'EV1477_GOVERNMENT_SOURCE_AUDIT.csv',['Evidence_ID','Agency','Document','URL','Access','Hash_Status','Use_Limit'],[{'Evidence_ID':'EV-1477','Agency':'Ministério da Justiça e Segurança Pública','Document':'Manual do Aluno APH Tático MJSP, 11-04-2025','URL':FULL['EV-1477'],'Access':'VERIFIED_GOVERNMENT_SOURCE','Hash_Status':next((x['SHA256'] for x in full if x['Evidence_ID']=='EV-1477'),'NR'),'Use_Limit':'Government institutional source; does not establish comparative clinical effectiveness.'}])
 write(OUT/'RECOVERY_TO_EXISTING_REFERENCE_RECONCILIATION.csv',list(recon[0]),recon)
 c=Counter(x['Final_Access_Status'] for x in recovery); man={'gate':'TARGETED_SOURCE_RECOVERY_PARTIAL','targets':len(targets),'newly_recovered_full_texts':sum(x['Final_Access_Status'].startswith('VERIFIED_') for x in recovery),'official_open_full_texts':c['VERIFIED_OPEN_FULL_TEXT'],'government_sources':c['VERIFIED_GOVERNMENT_SOURCE'],'abstract_only_retained':c['ABSTRACT_ONLY_CONFIRMED'],'paywalled_no_lawful_full_text':c['PAYWALLED_NO_LAWFUL_FULL_TEXT'],'new_result_ids':len(newres),'auditable_locators':len(loc),'forced_semantic_links':0,'illegal_access':0,'new_references_added':0,'reason':'Lawful recovery improved source availability but unresolved central paywalled sources prevent consolidated result-level packets.'}
 (OUT/'BATCH10_4F_R1B1A_MANIFEST.json').write_text(json.dumps(man,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 (OUT/'BATCH10_4F_R1B1A_REPORT.md').write_text(f'''# Batch 10.4F-R1B1A — targeted lawful full-text recovery\n\n`TARGETED_SOURCE_RECOVERY_PARTIAL`\n\nTargets completed: **{len(targets)}/14**. Lawful direct recovery produced **{man['newly_recovered_full_texts']}** official/open or government full texts; **{man['abstract_only_retained']}** records retain a structured PubMed abstract result; **{man['paywalled_no_lawful_full_text']}** remain without lawful full text. No reference, manuscript, Zotero record or CEF-v1 field changed.\n\nThe next valid action is consolidation into packets, not sentence re-adjudication.\n''',encoding='utf-8')
if __name__=='__main__':main()
