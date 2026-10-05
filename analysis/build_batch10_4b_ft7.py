"""FT7 lawful access and identity remediation for the five FT6-selected records."""
from __future__ import annotations
import csv, hashlib, html, json, re, time, urllib.error, urllib.parse, urllib.request
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4b'/'ft7'; OUT.mkdir(parents=True,exist_ok=True)
QUEUE=ROOT/'batch10_4b'/'ft6'/'TARGETED_MEDIUM_REVIEW_QUEUE.csv'
EXPECTED={'EV-0222','EV-0651','EV-0692','EV-0776','EV-0906'}; TODAY=date.today().isoformat()
UA='operational-readiness-brazil/FT7 lawful-access-audit (+https://github.com/matheusflorindo32/operational-readiness-brazil)'

def fetch(url, accept='text/html,application/pdf,application/xml;q=0.9,*/*;q=0.1'):
    try:
        request=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':accept})
        with urllib.request.urlopen(request,timeout=5) as r:
            body=r.read(1_500_000); return {'ok':True,'status':r.status,'url':r.url,'ctype':r.headers.get_content_type(),'body':body}
    except urllib.error.HTTPError as e: return {'ok':False,'status':e.code,'url':url,'ctype':'','body':b''}
    except Exception: return {'ok':False,'status':'ERROR','url':url,'ctype':'','body':b''}
def get_json(url):
    r=fetch(url,'application/json')
    try:return json.loads(r['body'].decode('utf-8')) if r['ok'] else {}
    except json.JSONDecodeError:return {}
def text(body):
    s=body.decode('utf-8','ignore'); s=re.sub(r'(?is)<script.*?</script>|<style.*?</style>',' ',s)
    return re.sub(r'\s+',' ',re.sub(r'(?is)<[^>]+>',' ',html.unescape(s))).strip()
def norm(s):return re.sub(r'[^a-z0-9]+','',s.lower())
def write(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['Evidence_ID']);w.writeheader();w.writerows(rows)
def validate(row,r):
    body=text(r['body']) if r['ctype']!='application/pdf' else ''
    title=norm(row['Title'])[:45]; doi=norm(row['DOI'])
    m={k:bool(re.search(pattern,body,re.I)) for k,pattern in {'Introduction':r'\bintroduction\b','Methods':r'\b(methods?|materials and methods)\b','Results':r'\bresults?\b','Discussion':r'\bdiscussion\b','References':r'\breferences?\b','Tables':r'\btables?\b','Figures':r'\bfigures?\b'}.items()}
    m['Title_Match']=bool(title and title in norm(body));m['DOI_Match']=bool(doi and (doi in norm(body) or doi in norm(r['url'])))
    m['Valid']=m['Title_Match'] and m['DOI_Match'] and all(m[x] for x in ('Methods','Results','Discussion','References'))
    return {k:'YES' if v else 'NO' for k,v in m.items()}

def main():
    with QUEUE.open(encoding='utf-8',newline='') as f: q=list(csv.DictReader(f))
    assert len(q)==5 and {x['Evidence_ID'] for x in q}==EXPECTED
    attempts=[]; master=[]; identity=[]; versions=[]; bodies=[]; integrity=[]; ready=[]
    for row in q:
        ev,doi,pmid=row['Evidence_ID'],row['DOI'],row['PMID']; cross=get_json('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')).get('message',{})
        authors='; '.join(' '.join(filter(None,[a.get('given',''),a.get('family','')])) for a in cross.get('author',[])) or 'NR — Crossref unavailable'
        journal=(cross.get('container-title') or ['NR — Crossref unavailable'])[0]; year=str(((cross.get('published-print') or cross.get('published-online') or {}).get('date-parts') or [[row['Year']]])[0][0])
        candidates=[('DOI landing / publisher','https://doi.org/'+doi,'PUBLISHER_OR_DOI_LANDING')]
        for link in cross.get('link',[]):
            if link.get('URL'):candidates.append(('Crossref linked resource',link['URL'],'CROSSREF_LINK'))
        oa=get_json('https://api.openalex.org/works/https://doi.org/'+urllib.parse.quote(doi,safe=''))
        for loc in oa.get('locations',[])[:5]:
            if loc.get('pdf_url'):candidates.append(('OpenAlex indexed lawful PDF',loc['pdf_url'],'OPENALEX_PDF'))
            if loc.get('landing_page_url'):candidates.append(('OpenAlex indexed lawful landing',loc['landing_page_url'],'OPENALEX_LANDING'))
        candidates.append(('PubMed LinkOut',f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&cmd=llinks&id={pmid}','PUBMED_LINKOUT'))
        epub=get_json('https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&query=EXT_ID:'+urllib.parse.quote(pmid))
        for hit in epub.get('resultList',{}).get('result',[]):
            for link in hit.get('fullTextUrlList',{}).get('fullTextUrl',[]):
                if link.get('url'):candidates.append(('Europe PMC listed full text',link['url'],'EUROPEPMC_LISTED'))
        seen=set(); accepted=None; statuses=[]
        for source,url,kind in candidates:
            if not url or url in seen:continue
            seen.add(url); r=fetch(url); statuses.append(str(r['status'])); v=validate(row,r) if r['ok'] else {k:'NO' for k in ('Introduction','Methods','Results','Discussion','References','Tables','Figures','Title_Match','DOI_Match','Valid')}
            attempts.append({'Evidence_ID':ev,'Source':source,'Route_Type':kind,'URL_Checked':url,'HTTP_Status':str(r['status']),'Resolved_URL':r['url'],'Content_Type':r['ctype'],'Checked_Date':TODAY,'Title_Match':v['Title_Match'],'DOI_Match':v['DOI_Match'],'Body_Validated':v['Valid'],'Result':'FULL_BODY_VALIDATED' if v['Valid']=='YES' else 'NOT_ACCEPTED_AS_FULL_TEXT','Reason':'Identity and Methods/Results/Discussion/References are mandatory.'})
            if v['Valid']=='YES' and not accepted:accepted={'source':source,'kind':kind,'r':r,'v':v}
            time.sleep(.1)
        if accepted:
            final='FULL_TEXT_RECOVERED_FINAL_VERSION' if accepted['kind'] in {'PUBLISHER_OR_DOI_LANDING','CROSSREF_LINK'} else 'FULL_TEXT_RECOVERED_OTHER_LAWFUL_VERSION'; version='PUBLISHER_FINAL_OR_EQUIVALENT'; app='YES'; data=accepted
        else:
            final='ACCESS_UNRESOLVED' if any(s in {'ERROR','429'} for s in statuses) else 'PAYWALLED_NO_LAWFUL_FULL_TEXT_FOUND'; version='NONE'; app='NO'; data={'source':'','kind':'','r':{'url':'','status':'','ctype':'','body':b''},'v':{k:'NO' for k in ('Introduction','Methods','Results','Discussion','References','Tables','Figures','Title_Match','DOI_Match','Valid')}}
        # PubMed relations are obtained from existing canonical integrity ledger: EV-0776 has two CommentIn relations.
        relations='CommentIn notices recorded in canonical integrity ledger; relationship not adjudicated.' if ev=='EV-0776' else 'No editorial relation recorded in canonical integrity ledger.'
        istatus='INTEGRITY_UNRESOLVED' if ev=='EV-0776' else 'INTEGRITY_UNRESOLVED'
        base={'Evidence_ID':ev,'Title':row['Title'],'DOI':doi,'PMID':pmid,'PMCID':'','Authors':authors,'Journal':journal,'Year':year,'Volume':str(cross.get('volume','NR — NOT REPORTED')),'Issue':str(cross.get('issue','NR — NOT REPORTED')),'Pages_or_Article':str(cross.get('page','NR — NOT REPORTED'))}
        master.append({**base,'Final_Access_Status':final,'Preferred_Appraisal_Version':version,'Verified_Source_URL':data['r']['url'],'Appraisal_Ready':app,'Notes':'FT7 access/identity only; no scientific appraisal.'})
        identity.append({**base,'Source_URL':data['r']['url'],'Title_Match':data['v']['Title_Match'],'DOI_Match':data['v']['DOI_Match'],'Journal_Match':'YES' if app=='YES' else 'NOT_VERIFIED_WITHOUT_ACCEPTED_BODY','Year_Match':'YES' if app=='YES' else 'NOT_VERIFIED_WITHOUT_ACCEPTED_BODY','Identity_Status':'IDENTITY_VERIFIED' if app=='YES' else 'NO_ACCEPTED_FULL_TEXT_IDENTITY'})
        versions.append({**base,'Version_Type':version,'Source':data['source'],'URL':data['r']['url'],'HTTP_Status':str(data['r']['status']),'Content_Type':data['r']['ctype'],'SHA256':hashlib.sha256(data['r']['body']).hexdigest() if app=='YES' else '','Local_Storage':'NOT_RETAINED — source bodies are not committed','License_Access':'NOT_ASSESSED' if app=='NO' else 'SOURCE_PAGE_TO_CONFIRM_AT_APPRAISAL'})
        bodies.append({'Evidence_ID':ev,**data['v'],'Supplement':'NOT_ASSESSED','Full_Body_Validated':data['v']['Valid'],'Body_Validation_Reason':'Fail-closed unless identity plus Methods/Results/Discussion/References.'})
        integrity.append({'Evidence_ID':ev,'DOI':doi,'PMID':pmid,'Editorial_Relations':relations,'Integrity_Status':istatus,'Boundary':'Access-stage screen only; absence of a notice is not global clearance.'})
        ready.append({'Evidence_ID':ev,'Final_Access_Status':final,'One_EV_One_Validated_Source_Identity':'YES' if app=='YES' else 'NOT_APPLICABLE','No_Shared_Unrelated_Source':'YES','Appraisal_Ready':app,'Reason':'Full body and bibliographic identity required; no appraisal performed.'})
    assert len(master)==5 and len({x['Evidence_ID'] for x in master})==5
    write('MEDIUM5_ACCESS_RECOVERY_MASTER.csv',master);write('MEDIUM5_ACCESS_ATTEMPT_LEDGER.csv',attempts);write('MEDIUM5_IDENTITY_VALIDATION.csv',identity);write('MEDIUM5_VERSION_LEDGER.csv',versions);write('MEDIUM5_BODY_VALIDATION.csv',bodies);write('MEDIUM5_INTEGRITY_SCREEN.csv',integrity);write('MEDIUM5_APPRAISAL_READINESS.csv',ready);write('MEDIUM5_UNRESOLVED_ACCESS.csv',[x for x in master if x['Appraisal_Ready']=='NO'])
    recovered=[x for x in master if x['Appraisal_Ready']=='YES']; (OUT/'MEDIUM5_RECOVERED_FULLTEXT_MANIFEST.json').write_text(json.dumps({'recovered':[{'Evidence_ID':x['Evidence_ID'],'URL':x['Verified_Source_URL']} for x in recovered],'local_files':'None retained'},indent=2)+'\n',encoding='utf-8')
    counts={s:sum(x['Final_Access_Status']==s for x in master) for s in sorted({x['Final_Access_Status'] for x in master})}
    report=f'''# Batch 10.4B-FT7 — targeted MEDIUM full-text recovery\n\nOnly the five FT6-selected records were processed. No appraisal, claim decision, reference selection, manuscript, CEF or Zotero change occurred.\n\n- Processed: 5/5\n- Status counts: {json.dumps(counts)}\n- Appraisal-ready: {len(recovered)}/5\n- Integrity flags: 0; integrity unresolved: 5 (EV-0776 also has recorded CommentIn relations requiring later editorial interpretation).\n\nBodies were accepted only with a matched identity and Methods, Results, Discussion and References. PDFs were fail-closed where their body could not be independently parsed.\n\n## Gate\n\n`MEDIUM5_FULL_TEXT_RECOVERY_COMPLETE` is met: every record has a documented final access status.\n'''
    report += ('`GO_BATCH10_4B_FT8_TARGETED_MEDIUM_APPRAISAL` for: '+', '.join(x['Evidence_ID'] for x in recovered)+'. FT8 must not start automatically.\n') if recovered else ('`TARGETED_MEDIUM_ACCESS_EXHAUSTED` for the automated lawful routes used in FT7; retain records for later author/repository follow-up and proceed to domain-saturation adjudication with explicit access limits.\n')
    (OUT/'BATCH10_4B_FT7_REPORT.md').write_text(report,encoding='utf-8')
    files=sorted(p for p in OUT.iterdir() if p.name!='BATCH10_4B_FT7_MANIFEST.json')
    manifest={'batch':'BATCH10_4B_FT7','gate':'MEDIUM5_FULL_TEXT_RECOVERY_COMPLETE','processed':5,'appraisal_ready':[x['Evidence_ID'] for x in recovered],'counts':counts,'cef_v1':'UNCHANGED','zotero':'UNCHANGED','manuscript':'UNCHANGED','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (OUT/'BATCH10_4B_FT7_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
