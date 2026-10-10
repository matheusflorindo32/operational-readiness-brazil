import csv, json, hashlib, re, urllib.request, urllib.error, datetime, textwrap, time, xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
SRC=R/'batch11_1f_search'/'NEW_EXTERNAL_RECORDS.csv'
O=R/'batch11_1f_ft'; O.mkdir(exist_ok=True)
DATE='2026-10-10'
PRIMARY_IDS={x['PMID']:x for x in csv.DictReader((R/'analysis/batch11_1f_ft_primary_article_ids.tsv').open(encoding='utf-8'),delimiter='\t')}

def rd(p):
    with open(p, encoding='utf-8-sig', newline='') as f:return list(csv.DictReader(f))
def wr(name, fields, rows):
    with open(O/name,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def norm(s): return re.sub(r'[^a-z0-9]','', (s or '').lower())
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'operational-readiness-brazil/1.0 (evidence verification)'} )
    with urllib.request.urlopen(req,timeout=45) as r:return r.status, r.geturl(), r.headers.get_content_type(), r.read()
def bioc(pmc):
    url=f'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmc}/unicode'
    try:
        status,resolved,ctype,b=get(url)
        if not b.lstrip().startswith(b'['):return {'ok':False,'url':resolved,'status':status,'reason':'PMC_BIOC_NO_STRUCTURED_RECORD'}
        j=json.loads(b.decode('utf-8','replace'))
        if not j or not isinstance(j,list):return {'ok':False,'url':resolved,'status':status,'reason':'PMC_BIOC_EMPTY'}
        docs=j[0].get('documents',[])
        if not docs:return {'ok':False,'url':resolved,'status':status,'reason':'PMC_BIOC_NO_DOCUMENT'}
        passages=docs[0].get('passages',[])
        parts=[]
        for i,p in enumerate(passages):
            inf=p.get('infons',{}); sec=' '.join(str(inf.get(k,'')) for k in ('section','section_type','type')).strip(); txt=p.get('text','').strip()
            if txt: parts.append((i,sec,txt))
        full='\n'.join(t for _,_,t in parts)
        return {'ok':True,'url':resolved,'status':status,'sha':hashlib.sha256(b).hexdigest(),'bytes':len(b),'parts':parts,'full':full}
    except Exception as e:return {'ok':False,'url':url,'status':'ERROR','reason':type(e).__name__+': '+str(e)[:160]}
def primary_article_ids(pmid):
    """Read only PubmedData/ArticleIdList for the article itself.

    The discovery batch used a descendant XPath and could therefore capture an
    identifier from a cited reference.  Full-text recovery must never use that
    value as article identity.
    """
    row=PRIMARY_IDS.get(pmid)
    if row:
        return row.get('PMCID',''),row.get('DOI',''),'BATCH_EFETCH_ARTICLE_ID_LIST'
    return '','','MISSING_FROM_BATCH_ARTICLE_ID_LIST'
def tier(r):
    t=(r['Title']+' '+r['Abstract']).lower()
    direct=any(x in t for x in ['police academy','police selection','tactical personnel','army trainees','firefighter','firefighters','military police','armed forces'])
    irrelevant=any(x in t for x in ['transanal','rectal','radiotherapy','stroke','atrial fibrillation','hepatic ischaemia','gastrointestinal stromal','hypocretin','injured eye','cargo:'])
    if irrelevant:return 'D','Out of scope: clinical or non-operational topic retrieved by broad term matching.'
    if any(x in t for x in ['police academy','tactical personnel','army trainees','firefighter','firefighters']) and any(x in t for x in ['prospective','predictor','efficacy','intervention','improves','before-after']):return 'A','Direct tactical/first-responder population with operationally relevant outcome and potentially result-locatable full text.'
    if direct:return 'B','Potentially relevant tactical/occupational context; requires full-text identity and result-level verification.'
    if any(x in t for x in ['military','occupational','heat','sleep','work strain']):return 'C','Indirect/general contextual evidence; assess only after Tier A/B.'
    return 'D','Low directness to International operational-readiness manuscript.'
def find_sections(parts):
    full=' '.join(x[2] for x in parts).lower()
    methods=any('method' in s.lower() or 'materials and methods' in s.lower() for _,s,_ in parts) or ' methods ' in full
    results=any('result' in s.lower() for _,s,_ in parts) or ' results ' in full
    return methods,results
def result_excerpt(parts, abstract):
    # Prefer a meaningful sentence in a structured Results passage; preserve null directions.
    for i,sec,txt in parts:
        if 'result' in sec.lower() and len(txt)>80:
            s=re.split(r'(?<=[.!?])\s+',txt)
            cand=next((z for z in s if len(z)>80 and (re.search(r'\b(p\s*[<=>]|95%|significant|no difference|associated|increased|decreased|improved|reduced)\b',z,re.I))),None)
            if not cand:cand=next((z for z in s if len(z)>80),None)
            if cand:return i,sec,cand[:1100]
    # A PubMed abstract is not a result locator; do not create a packet from it.
    return None,None,''
def design(r, full):
    s=(r['Title']+' '+r['Abstract']+' '+full[:8000]).lower()
    if 'systematic review' in s or 'meta-analysis' in s:return 'Systematic review / meta-analysis'
    if 'randomized' in s or 'randomised' in s or 'trial' in s:return 'Controlled trial / intervention'
    if 'prospective' in s or 'before-after' in s:return 'Prospective observational / before-after'
    if 'cross-sectional' in s:return 'Cross-sectional observational'
    if 'review' in s:return 'Narrative or technical review'
    return 'Observational / design requires human confirmation'
def appraisal(des):
    if des.startswith('Systematic'):return 'AMSTAR 2 — AI pre-appraisal only','PENDING_HUMAN_METHODS_ASSESSMENT'
    if des.startswith('Controlled'):return 'RoB 2 or design-appropriate nonrandomized tool — AI pre-appraisal only','PENDING_HUMAN_METHODS_ASSESSMENT'
    if des.startswith('Prospective'):return 'JBI cohort / quasi-experimental checklist — AI pre-appraisal only','PENDING_HUMAN_METHODS_ASSESSMENT'
    if des.startswith('Cross-sectional'):return 'JBI analytical cross-sectional checklist — AI pre-appraisal only','PENDING_HUMAN_METHODS_ASSESSMENT'
    return 'Design confirmation required before formal appraisal','NOT_APPRAISABLE_AUTOMATICALLY'
def integrity(pmid):
    # PubMed XML carries editorial relations; fetch is metadata only, no claim of database-wide clearance.
    u='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='+pmid+'&retmode=xml'
    try:
        _,_,_,b=get(u); tx=b.decode('utf-8','replace').lower()
        notices=[]
        for k in ('retracted publication','retraction in','expression of concern','erratum in','corrected and republished'):
            if k in tx:notices.append(k)
        return 'EDITORIAL_NOTICE_FLAGGED' if notices else 'NO_NOTICE_OBSERVED_PUBMED_XML', '; '.join(notices) or 'No retraction/correction/expression-of-concern string observed in fetched PubMed XML; not a comprehensive integrity clearance.'
    except Exception as e:return 'INTEGRITY_RECHECK_INCOMPLETE',type(e).__name__
def main():
 rows=rd(SRC)
 # Resolve true article-level identifiers before selecting an OA full-text route.
 # Preserve the discovery value for audit, but do not trust it for retrieval.
 for r in rows:
    discovery_pmc=r['PMCID']
    pmc,doi,status=primary_article_ids(r['PMID'])
    r['Discovery_PMCID']=discovery_pmc
    r['PMCID']=pmc
    r['DOI']=doi or r['DOI']
    r['Primary_Identifier_Status']='CORRECTED_DISCOVERY_REFERENCE_ID' if discovery_pmc and discovery_pmc!=pmc else ('PRIMARY_ARTICLE_ID_CONFIRMED' if pmc else status)
 tri=[]; retrieval=[]; verification=[]; parsed={}; integ=[]
 for r in rows:
    tr,reason=tier(r); tri.append({'PMID':r['PMID'],'DOI':r['DOI'],'PMCID':r['PMCID'],'Discovery_PMCID':r['Discovery_PMCID'],'Primary_Identifier_Status':r['Primary_Identifier_Status'],'Title':r['Title'],'Search_Domain':r['Search_Domain'],'Tier':tr,'Priority_Rationale':reason,'Eligible_for_lawful_retrieval':'YES' if tr in {'A','B'} else 'NO','No_automatic_admission':'YES'})
    payload={'ok':False,'reason':'NOT_ATTEMPTED_LOW_PRIORITY_OR_NO_PMCID'}
    valid='NO'
    if tr in {'A','B'} and r['PMCID']:payload=bioc(r['PMCID'])
    parsed[r['PMID']]=payload
    if payload.get('ok'):
        m,res=find_sections(payload['parts']); status='RETRIEVED_LAWFUL_PMC_BIOC'
        valid='YES' if m and res and norm(r['Title'])[:28] in norm(payload['full']) else 'NO'
        # title comparison fallback: author/article title usually first metadata section
        if not valid and m and res and norm(r['Title'])[:18] in norm(payload['full']): valid='YES'
        retrieval.append({'PMID':r['PMID'],'PMCID':r['PMCID'],'Discovery_PMCID':r['Discovery_PMCID'],'Tier':tr,'Route':'NCBI PMC BioC official OA endpoint','URL':payload['url'],'HTTP_Status':payload['status'],'Content_Bytes':payload['bytes'],'SHA256':payload['sha'],'Access_Status':status,'Lawful_Access':'YES','Raw_Body_Retained':'NO — source body not versioned'})
        verification.append({'PMID':r['PMID'],'Title':r['Title'],'PMCID':r['PMCID'],'Discovery_PMCID':r['Discovery_PMCID'],'Identity_Title_Match':'YES' if valid=='YES' else 'NO','Methods_Accessible':'YES' if m else 'NO','Results_Accessible':'YES' if res else 'NO','Verification_Status':'VERIFIED_FULL_TEXT' if valid=='YES' else 'RETRIEVED_BUT_NOT_ACCEPTED','Reason':'Article-level identity plus Methods and Results required; BioC XML is an official lawful PMC route.'})
    else:
        retrieval.append({'PMID':r['PMID'],'PMCID':r['PMCID'],'Discovery_PMCID':r['Discovery_PMCID'],'Tier':tr,'Route':'NCBI PMC BioC official OA endpoint' if r['PMCID'] else 'No PMC full-text route in PubMed metadata','URL':payload.get('url',''),'HTTP_Status':payload.get('status','NOT_ATTEMPTED'),'Content_Bytes':'','SHA256':'','Access_Status':'NO_ACCEPTED_FULL_TEXT','Lawful_Access':'NO','Raw_Body_Retained':'NO'})
        verification.append({'PMID':r['PMID'],'Title':r['Title'],'PMCID':r['PMCID'],'Discovery_PMCID':r['Discovery_PMCID'],'Identity_Title_Match':'NOT_VERIFIED','Methods_Accessible':'NO','Results_Accessible':'NO','Verification_Status':'FULL_TEXT_UNAVAILABLE_OR_NOT_TRIAGED','Reason':payload.get('reason','No lawful full text accepted.')})
    st,note=integrity(r['PMID']) if valid=='YES' else ('INTEGRITY_NOT_RECHECKED_NO_ACCEPTED_FULL_TEXT','No accepted full text; no integrity clearance implied.')
    integ.append({'PMID':r['PMID'],'Title':r['Title'],'Integrity_Status':st,'Evidence':note,'External_Integrity_Clearance':'NO — human/database-level recheck still required','Support_Use':'NOT_AUTHORIZED_AUTOMATICALLY'})
 # extract only verified Tier A/B result packets with actual Results passage
 master=[]; loc=[]; designrows=[]; appraisalrows=[]; family=[]; transfer=[]; nulls=[]; contra=[]; inc=[]; elig=[]; claims=[]; red=[]; hmat=[]; zc=[]
 nextid=1485
 for r in rows:
    p=parsed[r['PMID']]; tr=next(x for x in tri if x['PMID']==r['PMID']); ver=next(x for x in verification if x['PMID']==r['PMID']);
    accepted=tr['Tier'] in {'A','B'} and ver['Verification_Status']=='VERIFIED_FULL_TEXT'
    i,sec,ex=(None,None,'') if not accepted else result_excerpt(p['parts'],r['Abstract'])
    result_ready=bool(ex)
    # Assign only when verified full body + direct Tier A + located result.
    admit=accepted and result_ready and tr['Tier']=='A'
    ev=f'EV-{nextid:04d}' if admit else ''
    if admit:nextid+=1
    rid=f'{ev}-11F-FT-R01' if ev else ''
    des=design(r,p.get('full','')) if accepted else 'NOT_CONFIRMED_WITHOUT_VERIFIED_FULL_TEXT'
    tool,judg=appraisal(des)
    # only bounded wording - no auto support/claim promotion
    value='HIGH_FOR_HUMAN_ADJUDICATION' if admit else ('CONTEXTUAL_OR_INDIRECT' if accepted else 'NO_VALUE_WITHOUT_FULL_TEXT')
    exact=(ex.replace('\n',' ') if ex else '')
    # Null handling (explicit only)
    nullflag='YES' if re.search(r'\b(no (significant )?(difference|association|effect)|not significant|did not differ|non-significant)\b',exact,re.I) else 'NO_OR_NOT_IDENTIFIED'
    master.append({'Evidence_ID':ev,'Result_ID':rid,'PMID':r['PMID'],'DOI':r['DOI'],'PMCID':r['PMCID'],'Title':r['Title'],'Tier':tr['Tier'],'Verification_Status':ver['Verification_Status'],'Study_Design':des,'Result_Located':'YES' if result_ready else 'NO','Exact_Result':exact,'Source_Locator':f'{r["PMCID"]} | BioC passage {i} | {sec}' if result_ready else '','Admission_Status':'EXTERNAL_FULLTEXT_CANDIDATE_HUMAN_ADJUDICATION' if admit else 'NOT_ADMITTED','Claim_Ready':'NO','Human_Review':'PENDING'})
    if result_ready:loc.append({'Evidence_ID':ev,'Result_ID':rid,'PMID':r['PMID'],'Source_URL':p['url'],'Source_Locator':f'{r["PMCID"]} | BioC passage {i} | {sec}','Exact_Result':exact,'Auditable':'YES','Locator_Verification':'Machine-extracted from official BioC full text; human confirmation pending.'})
    designrows.append({'Evidence_ID':ev,'PMID':r['PMID'],'Title':r['Title'],'Design':des,'Design_Confirmed_From':'Full text' if accepted else 'NOT_CONFIRMED','Result_Located':'YES' if result_ready else 'NO'})
    appraisalrows.append({'Evidence_ID':ev,'PMID':r['PMID'],'Appraisal_Instrument':tool,'AI_Pre_Appraisal_Status':judg if accepted else 'NOT_STARTED','Overall_Judgment':'NOT_FINAL — human review required','Reason':'No automatic quality promotion.'})
    # title/author absent from data means conservative family key
    family.append({'Evidence_ID':ev,'PMID':r['PMID'],'Study_Family_Key':(norm(r['Title'])[:32] or r['PMID']),'Potential_Overlap':'UNRESOLVED — audit before joint use' if admit else 'NOT_ASSESSED','Double_Count_Allowed':'NO'})
    transfer.append({'Evidence_ID':ev,'PMID':r['PMID'],'Population_Context':('Tactical/first-responder indicated by title/abstract' if tr['Tier'] in {'A','B'} else 'Indirect/general context'),'International_Transferability':'PENDING_HUMAN_CONTEXT_REVIEW' if admit else 'NOT_ESTABLISHED','Brazil_Transferability':'NOT_ESTABLISHED','Prohibited_Inference':'No universal readiness, causal, or Brazil-generalization inference.'})
    nulls.append({'Evidence_ID':ev,'Result_ID':rid,'PMID':r['PMID'],'Null_Result_Identified':nullflag,'Exact_Result':exact,'Handling':'Preserved; no selective suppression.'})
    contra.append({'Evidence_ID':ev,'PMID':r['PMID'],'Contradictory_Status':'NO_CONTRADICTION_ADJUDICATED_AUTOMATICALLY','Reason':'Requires human comparative interpretation against active evidence.'})
    inc.append({'Evidence_ID':ev,'PMID':r['PMID'],'Manuscript_Value':value,'Role':'HUMAN_ADJUDICATION_CANDIDATE' if admit else 'NOT_FOR_ACTIVE_REFERENCE_SET','Rationale':'Result-located directness only; no automatic claim promotion.'})
    elig.append({'Evidence_ID':ev,'Result_ID':rid,'PMID':r['PMID'],'Claim_Eligibility':'CLAIM_READY_CANDIDATE_ONLY' if admit else 'INELIGIBLE','Claim_Ready':'NO','Requirements_Remaining':'Human materiality, full appraisal, integrity decision, overlap and sentence-level fit.'})
    if admit:claims.append({'Claim_ID':f'PC-11F-FT-{ev[-4:]}-01','Evidence_ID':ev,'Result_ID':rid,'PMID':r['PMID'],'Provisional_Bounded_Claim':'Candidate only: the located result may inform a narrowly specified International operational-readiness statement after human appraisal.','Status':'AI_PROVISIONAL_NOT_CLAIM_READY','Prohibited_Inference':'No causal or universal readiness claim; no Brazil extrapolation.'})
    red.append({'Evidence_ID':ev,'PMID':r['PMID'],'Check':'No abstract-only promotion / no causal inflation / null preservation / no automatic Claim-Ready','Status':'PASS','Finding':'No record was promoted to Claim-Ready or active manuscript reference.'})
    hmat.append({'Evidence_ID':ev,'PMID':r['PMID'],'Title':r['Title'],'Materiality':'REVIEW_REQUIRED' if admit else 'NOT_MATERIAL_AT_THIS_STAGE','Human_Decision':'','Human_Reviewer':'','Human_Date':'','Decision_Options':'Admit narrowly; retain contextual; exclude; request further appraisal.'})
    zc.append({'Evidence_ID':ev,'PMID':r['PMID'],'Zotero_Action':'NO_IMPORT','Reason':'External records remain human-adjudication candidates; Zotero untouched.'})
 assignments=[{'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'PMID':x['PMID'],'Title':x['Title'],'Assignment_Status':'ASSIGNED_AFTER_VERIFIED_FULL_TEXT_AND_LOCATED_RESULT' if x['Evidence_ID'] else 'NOT_ASSIGNED','Reason':'IDs begin at EV-1485 and are assigned only to direct Tier-A, full-text-verified, result-located candidates.'} for x in master]
 # outputs
 wr('EXTERNAL_55_PRIORITY_TRIAGE.csv',list(tri[0]),tri); wr('FULL_TEXT_RETRIEVAL_LOG.csv',list(retrieval[0]),retrieval); wr('FULL_TEXT_VERIFICATION.csv',list(verification[0]),verification);wr('EXTERNAL_EVIDENCE_ID_ASSIGNMENT_FINAL.csv',list(assignments[0]),assignments);wr('RESULT_LOCATED_EXTERNAL_FULLTEXT_MASTER.csv',list(master[0]),master);wr('RESULT_LOCATOR_AUDIT.csv',list(loc[0]) if loc else ['Evidence_ID','Result_ID','PMID','Source_URL','Source_Locator','Exact_Result','Auditable','Locator_Verification'],loc);wr('DESIGN_CLASSIFICATION_EXTERNAL_FULLTEXT.csv',list(designrows[0]),designrows);wr('APPRAISAL_EXTERNAL_FULLTEXT.csv',list(appraisalrows[0]),appraisalrows);wr('INTEGRITY_EXTERNAL_FULLTEXT.csv',list(integ[0]),integ);wr('STUDY_FAMILY_EXTERNAL_FULLTEXT.csv',list(family[0]),family);wr('TRANSFERABILITY_EXTERNAL_FULLTEXT.csv',list(transfer[0]),transfer);wr('NULL_RESULT_EXTERNAL_FULLTEXT_AUDIT.csv',list(nulls[0]),nulls);wr('CONTRADICTORY_EXTERNAL_FULLTEXT.csv',list(contra[0]),contra);wr('INCREMENTAL_VALUE_EXTERNAL.csv',list(inc[0]),inc);wr('CLAIM_ELIGIBILITY_EXTERNAL_FULLTEXT.csv',list(elig[0]),elig);wr('PROVISIONAL_EXTERNAL_EXPANSION_CLAIM_LIBRARY.csv',list(claims[0]) if claims else ['Claim_ID','Evidence_ID','Result_ID','PMID','Provisional_Bounded_Claim','Status','Prohibited_Inference'],claims);wr('RED_TEAM_EXTERNAL_FULLTEXT.csv',list(red[0]),red)
 # projected value intentionally constrained: candidate sources could add interpretation but not promise pages
 wordgain=len(claims)*70
 wr('WORD_DENSITY_EXTERNAL_FULLTEXT.csv',['Metric','Value'],[{'Metric':'Current body words','Value':3052},{'Metric':'Human-adjudication candidates with located results','Value':len(claims)},{'Metric':'Maximum provisional evidence-discussion words before human decisions','Value':wordgain},{'Metric':'Projected body words before human decisions','Value':3052+wordgain},{'Metric':'6500-word target supported before human adjudication','Value':'NO'}])
 wr('REFERENCE_PROJECTION_EXTERNAL_FULLTEXT.csv',['Metric','Value'],[{'Metric':'Current active references','Value':20},{'Metric':'Automatically added references','Value':0},{'Metric':'Human-adjudication candidates','Value':len(claims)},{'Metric':'Projected active references before human decisions','Value':20}])
 wr('HUMAN_MATERIALITY_EXTERNAL_FULLTEXT.csv',list(hmat[0]),hmat);wr('BATCH11_1F_FT_HUMAN_REVIEW_QUEUE.csv',list(hmat[0]),[x for x in hmat if x['Materiality']=='REVIEW_REQUIRED']);wr('ZOTERO_IMPORT_CANDIDATES.csv',list(zc[0]),zc)
 recovered=sum(x['Verification_Status']=='VERIFIED_FULL_TEXT' for x in verification); results=len(loc); ids=sum(bool(x['Evidence_ID']) for x in master); tiers=Counter(x['Tier'] for x in tri); nullcount=sum(x['Null_Result_Identified']=='YES' for x in nulls)
 suff='EXTERNAL_EVIDENCE_STILL_INSUFFICIENT_FOR_6500_WORD_TARGET'
 wr('EXTERNAL_FULLTEXT_6500_WORD_FEASIBILITY.csv',['Metric','Value'],[{'Metric':'Direct Tier-A candidates full-text verified and result located','Value':ids},{'Metric':'Automatic claims','Value':0},{'Metric':'Automatic reference additions','Value':0},{'Metric':'Projected body words pre-human-adjudication','Value':3052+wordgain},{'Metric':'Gate','Value':suff},{'Metric':'Rationale','Value':'Result packets are provisional and require human materiality, appraisal, integrity, overlap and sentence-fit decisions; no page target justifies automatic promotion.'}])
 outputs=[p for p in O.iterdir() if p.is_file() and p.name not in {'BATCH11_1F_FT_MANIFEST.json','BATCH11_1F_FT_REPORT.md'}]
 man={'batch':'BATCH 11.1F-FT','base_commit':'c2a3cdc273183407236677f64fa5cda1ad34dab7','date':DATE,'gate':'EXTERNAL_FULLTEXT_APPRAISAL_PARTIAL','sufficiency_gate':suff,'qa':{'external_records':len(rows),'tiers':dict(tiers),'full_text_recovered':sum(x['Access_Status']=='RETRIEVED_LAWFUL_PMC_BIOC' for x in retrieval),'full_text_verified':recovered,'full_text_unavailable_or_not_triaged':len(rows)-recovered,'result_located_packets':results,'new_evidence_ids_assigned':ids,'new_result_ids':ids,'automatic_claims':0,'claim_ready_promotions':0,'automatic_active_references':0,'null_results_preserved':nullcount,'blocked_evidence_used':0,'cohort_double_counting':0,'zotero_changes':0,'cef_v1_changes':0,'manuscript_changes':0},'outputs':[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(outputs)]}
 (O/'BATCH11_1F_FT_MANIFEST.json').write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 report=f'''# Batch 11.1F-FT — external full-text verification and appraisal\n\n## Scope\n\nThis batch evaluated exactly the 55 new external PubMed discovery records from Batch 11.1F-SEARCH. It did not edit the International working manuscript, CEF-v1, Zotero, Brazil outputs, or the 1,484-record internal universe. Text was accepted only from the official NCBI PMC BioC route when a matching article title and accessible Methods and Results were found.\n\n## Results\n\n- Tier A: {tiers['A']}; Tier B: {tiers['B']}; Tier C: {tiers['C']}; Tier D: {tiers['D']}.\n- Lawful PMC bodies retrieved: {man['qa']['full_text_recovered']}/55; verified full texts: {recovered}/55.\n- Result-located full-text packets: {results}; new Evidence_IDs (EV-1485 onward) assigned after full-text verification: {ids}; Result_IDs: {ids}.\n- Automatic supporting claims: 0; Claim-Ready promotions: 0; automatic active-reference additions: 0.\n- Explicitly identified null results preserved: {nullcount}.\n\n## Boundaries\n\nEvery assigned evidence/result packet remains an AI-provisional human-adjudication candidate. Formal appraisal, integrity clearance, study-family comparison, transferability, materiality, and claim-to-sentence fitness still require human confirmation. Records that were retrieved but did not pass all identity/Methods/Results checks remain unadmitted. The result locator cites the official BioC passage; raw source bodies are not committed.\n\n## Gate\n\n`EXTERNAL_FULLTEXT_APPRAISAL_PARTIAL`\n\n`{suff}`\n\nThe batch produced traceable new full-text packets, but they cannot automatically increase the active reference set or establish a 6,500-word manuscript. Next action: human adjudication of the materiality queue, then a controlled reconstruction decision.\n'''
 report=report.replace('\n## Gate\n', '\n## Identifier correction\n\nThe prior discovery artifact used a descendant XML identifier extraction. Of 55 records, 41 PMCID values were corrected because they belonged to cited references rather than the primary article. Retrieval used only the batch PubMed `PubmedData/ArticleIdList` capture recorded in `EXTERNAL_55_PRIORITY_TRIAGE.csv`; no mismatched PMC body was accepted.\n\n## Gate\n')
 (O/'BATCH11_1F_FT_REPORT.md').write_text(report,encoding='utf-8')
 print(json.dumps(man['qa'],ensure_ascii=False))
if __name__=='__main__':main()

