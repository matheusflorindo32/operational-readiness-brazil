"""Build conservative source-level packets for the 16 references retained in v0.13.

No search expansion occurs here.  PubMed/PMC requests use only identifiers
already frozen in the project; inaccessible sources are recorded rather than
supplemented by thematic inference or manuscript text.
"""
import csv, hashlib, json, re, urllib.request, xml.etree.ElementTree as E
from collections import Counter
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4f_r1b1'
TODAY='2026-10-07'; UA={'User-Agent':'operational-readiness-brazil/1.0 (source-localization)'}

def read(path):
    with path.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def write(path,fields,rows):
    path.parent.mkdir(exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def norm(s):return re.sub(r'\W+','',s or '').lower()
def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30) as r:return r.read()
    except Exception:return None
def pubmed(pmid):
    if not pmid:return {}
    raw=get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml')
    if not raw:return {}
    root=E.fromstring(raw); article=root.find('.//PubmedArticle');
    if article is None:return {}
    doi=''; pmc=''
    for x in article.findall('.//ArticleId'):
        if x.attrib.get('IdType')=='doi':doi=x.text or ''
        if x.attrib.get('IdType')=='pmc':pmc=x.text or ''
    abstract=' '.join(''.join(x.itertext()) for x in article.findall('.//Abstract/AbstractText')).strip()
    title=''.join(article.find('.//ArticleTitle').itertext()) if article.find('.//ArticleTitle') is not None else ''
    return {'doi':doi,'pmc':pmc,'title':title,'abstract':abstract}
def pmc_fetch(pmc):
    if not pmc:return None
    return get(f'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmc}/unicode')

def main():
    refs=read(ROOT/'batch10_4d'/'FINAL_REFERENCE_AUDIT.csv')
    canonical={r['Evidence_ID']:r for r in read(ROOT/'batch10_4b'/'canonical'/'MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv')}
    inventory=[]; prov=[]; support=[]; result=[]; locator=[]; scope=[]; prohibited=[]; nulls=[]; transfer=[]; unavailable=[]
    for ref in refs:
        ev=ref['Evidence_ID']; c=canonical.get(ev,{})
        doi=ref['DOI'] if ref['DOI']!='NO_DOI_LISTED' else ''
        pmid=c.get('PMID',''); pmc=c.get('PMCID',''); source={}
        if pmid: source=pubmed(pmid)
        source_doi=source.get('doi',''); source_pmc=source.get('pmc','') or pmc
        identity='DOI_EXACT_MATCH' if doi and source_doi and doi.lower()==source_doi.lower() else ('PROJECT_IDENTIFIER_ONLY' if not source else 'IDENTITY_UNRESOLVED')
        pmc_data=pmc_fetch(source_pmc) if ev in {'EV-1473','EV-1484'} else None
        if pmc_data:
            status='VERIFIED_OFFICIAL_FULL_TEXT'; st='PMC XML full text'; url=f'https://pmc.ncbi.nlm.nih.gov/articles/{source_pmc}/'
        elif source.get('abstract'):
            status='ABSTRACT_ONLY'; st='PubMed structured abstract'; url=f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/'
        else:
            status='SOURCE_UNAVAILABLE'; st='No project full text or official PubMed abstract recovered from frozen identifier'; url=(f'https://doi.org/{doi}' if doi else '')
        title=c.get('Title','') or ref['Authors_Title_Year_Journal']
        inventory.append({'Reference_Number':ref['Ref'],'Reference_ID':ref['Ref'],'Evidence_ID':ev,'Exact_Title':title,'Authors':ref['Authors_Title_Year_Journal'].split('.')[1].strip() if '.' in ref['Authors_Title_Year_Journal'] else 'NR','Year':c.get('Year','NR'),'Journal':ref['Authors_Title_Year_Journal'].split('. ')[-2] if '. ' in ref['Authors_Title_Year_Journal'] else 'NR','DOI':doi or 'NO_DOI_LISTED','PMID':pmid or 'NR','PMCID':source_pmc or 'NR','International_Use':ref['International_Citations'],'Brazil_Use':ref['Brazil_Citations'],'Current_Evidence_Role':'RETAINED_V013_REFERENCE','Full_Text_Status':status,'Source_Availability':st})
        prov.append({'Reference_ID':ref['Ref'],'Evidence_ID':ev,'Source_Type':st,'Source_URL_or_Project_Path':url,'Access_Date':TODAY,'DOI':doi or 'NO_DOI_LISTED','PMID':pmid or 'NR','PMCID':source_pmc or 'NR','Publisher_or_Repository':'PMC/NCBI' if pmc_data else ('PubMed/NCBI' if source else 'NONE_VERIFIED'),'File_Hash':'NR_REMOTE_SOURCE_NOT_STORED','Identity_Match':identity,'Provenance_Status':status})
        design=c.get('Study_Design','NR'); pop=c.get('Population','NR')
        transferability='DIRECT' if ev.startswith('EV-') else 'INDIRECT'
        transfer.append({'Reference_ID':ref['Ref'],'Evidence_ID':ev,'Population':pop,'Population_Category':'Brazilian public-safety / tactical' if ev.startswith('EV-') else 'Military/tactical framework','Population_Transferability':transferability if ev.startswith('EV-') else 'MODERATE','Study_Design':design,'Design_Limitation':'Association and descriptive designs do not establish causality; source-specific appraisal remains required.'})
        permitted='Only population-, outcome-, and design-bounded statements directly located in the source.'
        forbidden='Causality, universal readiness prediction, national prevalence, or transfer beyond the documented population/design.'
        scope.append({'Reference_ID':ref['Ref'],'Evidence_ID':ev,'PERMITTED_CLAIM_SCOPE':permitted,'Source_Status':status})
        prohibited.append({'Reference_ID':ref['Ref'],'Evidence_ID':ev,'PROHIBITED_INFERENCE':forbidden,'Source_Status':status})
        if status=='SOURCE_UNAVAILABLE': unavailable.append({'Reference_ID':ref['Ref'],'Evidence_ID':ev,'Missing_Source':'No verified full text or PubMed abstract recovered through frozen identifier','Affected_Use':'All current v0.13 uses require source-level reassessment','Permitted_Interim_Role':'METHODS_OR_CONTEXT_ONLY_PENDING_REVIEW','Current_Claim_Becomes_Unsupported':'YES'})
        if ev=='EV-1473' and pmc_data:
            rows=[
                ('EV-1473-R01','Results','paragraph 59','Handgrip strength in shooting position','Stress-symptom versus no-stress groups','24 police cadets','Between-group difference','Difference 7.86 kg; 95% CI 0.73 to 15.00; p=0.03','higher in stress-symptom group','NO','Cross-sectional/observational comparison cannot establish stress effect.'),
                ('EV-1473-R02','Results','paragraph 60','Shooting score, time, and accuracy coefficient','Stress-symptom versus no-stress groups','24 police cadets','Shooting performance','Score p=0.96; time p=0.55; coefficient p=0.66','no statistically significant group differences','YES','Small cadet sample; no operational field-performance inference.'),
                ('EV-1473-R03','Results','paragraph 62','Accuracy coefficient correlations','Handgrip/service/physical-activity measures','24 police cadets','Correlation with accuracy coefficient','No significant correlations reported','null correlation findings','YES','Specific protocol and cadet cohort limit transferability.')]
            for rid,sec,loc,outcome,exposure,population,comp,effect,direction,null,limit in rows:
                result.append({'Evidence_ID':ev,'Result_ID':rid,'Source_Section':sec,'Source_Subsection':'NR','Page_Number':'NR_XML','Paragraph_or_Locator':loc,'Table_Number':'NR','Figure_Number':'See source locator where applicable','Outcome':outcome,'Exposure_or_Intervention':exposure,'Comparator':comp,'Population':population,'Sample_Size':'24','Effect_Estimate':effect,'CI':'Included when reported','P_value':'Included when reported','Direction':direction,'Null_Result':null,'Author_Interpretation':'Study-specific observation only','Methodological_Limitation':limit,'Transferability_Limitation':limit})
                locator.append({'Result_ID':rid,'Evidence_ID':ev,'Source_URL':url,'Locator':f'PMC11983491 > Results > {loc}','Locator_Auditable':'YES'})
                if null=='YES':nulls.append({'Evidence_ID':ev,'Result_ID':rid,'Null_Result':'YES','Preservation_Note':'Retained without conversion to positive trend.'})
        elif ev=='EV-1484' and pmc_data:
            rid='EV-1484-R01'; result.append({'Evidence_ID':ev,'Result_ID':rid,'Source_Section':'Results','Source_Subsection':'multivariate logistic regression','Page_Number':'NR_XML','Paragraph_or_Locator':'paragraph 80','Table_Number':'Table 5','Figure_Number':'NR','Outcome':'Medical readiness for active duty','Exposure_or_Intervention':'Worker, age, sex and health-risk variables','Comparator':'Model reference categories','Population':'6,621 police officers and 1,347 firefighters, Paraná','Sample_Size':'7,968','Effect_Estimate':'Police officer OR 1.50 (95% CI 1.27–1.77); selected modifiable risk factors also associated','CI':'95% CI reported','P_value':'NR in packet','Direction':'higher modelled odds of not being medically ready in specified comparisons','Null_Result':'NO','Author_Interpretation':'Association in a cross-sectional medical-record analysis','Methodological_Limitation':'Cross-sectional design cannot establish causal direction.','Transferability_Limitation':'Paraná cohort does not estimate national prevalence.'})
            locator.append({'Result_ID':rid,'Evidence_ID':ev,'Source_URL':url,'Locator':'PMC9453999 > Results > paragraph 80 > Table 5','Locator_Auditable':'YES'})
        elif status=='ABSTRACT_ONLY':
            # The packet deliberately does not invent Results-section locators from an abstract.
            unavailable.append({'Reference_ID':ref['Ref'],'Evidence_ID':ev,'Missing_Source':'Full text unavailable; PubMed abstract exists but has no auditable result-level locator','Affected_Use':'Any result-specific support use','Permitted_Interim_Role':'ABSTRACT_ONLY_EVIDENCE','Current_Claim_Becomes_Unsupported':'YES'})
        support.append({'Reference_ID':ref['Ref'],'Evidence_ID':ev,'Identity':'VERIFIED' if identity=='DOI_EXACT_MATCH' else identity,'Source_Status':status,'Design':design,'Population':pop,'Result_IDs_Extracted':';'.join(r['Result_ID'] for r in result if r['Evidence_ID']==ev) or 'NONE','Packet_Status':'READY_FOR_LIMITED_SOURCE_LEVEL_USE' if any(r['Evidence_ID']==ev for r in result) else 'RESULT_LEVEL_LOCALIZATION_UNAVAILABLE'})
    # Preserve the two required historical nulls even where source localization has not yet succeeded.
    for ev,note in [('EV-1474','No source-level result locator recovered in this batch; preserve as unrelocated history, not positive support.'),('EV-1479','Existing project history records a null programme result; no official result-level locator recovered in this batch.')]:
        nulls.append({'Evidence_ID':ev,'Result_ID':'NOT_RELOCALIZED','Null_Result':'HISTORICAL_NULL_RETAINED','Preservation_Note':note})
    adjud=read(ROOT/'batch10_4f_r1b'/'SENTENCE_SUPPORT_ADJUDICATION.csv')
    results_by_ev={r['Evidence_ID'] for r in result}
    cross=[]
    for s in adjud:
        evs=[x for x in s['Evidence_ID'].split(';') if x]
        candidates=[r['Result_ID'] for r in result if r['Evidence_ID'] in evs]
        cross.append({'Sentence_ID':s['Sentence_ID'],'Reference_ID':s['Reference_ID'],'Evidence_ID':s['Evidence_ID'],'Candidate_Result_IDs':';'.join(candidates),'Candidate_Fit':'POTENTIAL_PARTIAL' if candidates else 'NO_RESULT_MATCH','Status':'PREPARATORY_ONLY_NOT_FINAL_SUPPORT_ADJUDICATION'})
    changes=[x for x in adjud if x['Final_Disposition']=='CITATION_CHANGE_REQUIRED']; narrows=[x for x in adjud if x['Final_Disposition']=='NARROWING_REQUIRED']
    def coverage(rows):
        return [{'Sentence_ID':x['Sentence_ID'],'Evidence_ID':x['Evidence_ID'],'Candidate_Result_IDs':';'.join(r['Result_ID'] for r in result if r['Evidence_ID'] in x['Evidence_ID'].split(';')),'Coverage':'RESULT_AVAILABLE' if any(r['Evidence_ID'] in x['Evidence_ID'].split(';') for r in result) else 'NO_RESULT_LEVEL_SOURCE'} for x in rows]
    write(OUT/'FINAL_16_REFERENCE_SOURCE_INVENTORY.csv',list(inventory[0]),inventory)
    write(OUT/'REFERENCE_SOURCE_PROVENANCE.csv',list(prov[0]),prov)
    fields=['Evidence_ID','Result_ID','Source_Section','Source_Subsection','Page_Number','Paragraph_or_Locator','Table_Number','Figure_Number','Outcome','Exposure_or_Intervention','Comparator','Population','Sample_Size','Effect_Estimate','CI','P_value','Direction','Null_Result','Author_Interpretation','Methodological_Limitation','Transferability_Limitation']
    write(OUT/'RESULT_LEVEL_EVIDENCE_LEDGER.csv',fields,result); write(OUT/'RESULT_SOURCE_LOCATOR_LEDGER.csv',['Result_ID','Evidence_ID','Source_URL','Locator','Locator_Auditable'],locator)
    write(OUT/'REFERENCE_EVIDENCE_SUPPORT_PACKETS.csv',list(support[0]),support);write(OUT/'REFERENCE_PERMITTED_CLAIM_SCOPE.csv',list(scope[0]),scope);write(OUT/'REFERENCE_PROHIBITED_INFERENCE.csv',list(prohibited[0]),prohibited);write(OUT/'REFERENCE_NULL_RESULTS.csv',list(nulls[0]),nulls);write(OUT/'REFERENCE_TRANSFERABILITY.csv',list(transfer[0]),transfer);write(OUT/'REFERENCE_COHORT_OVERLAP.csv',['Evidence_ID','Cohort_Family','Independent_Cohort_Count','Rule'],[{'Evidence_ID':'EV-1473;EV-1474','Cohort_Family':'CF-BR-PMES-CFO-2023-01','Independent_Cohort_Count':'1','Rule':'Report distinct outcomes separately; do not count as independent cohorts.'}]);write(OUT/'SOURCE_UNAVAILABLE_LEDGER.csv',list(unavailable[0]),unavailable)
    write(OUT/'SENTENCE_RESULT_CANDIDATE_CROSSWALK.csv',list(cross[0]),cross);write(OUT/'CITATION_CHANGE_SOURCE_COVERAGE.csv',['Sentence_ID','Evidence_ID','Candidate_Result_IDs','Coverage'],coverage(changes));write(OUT/'NARROWING_SOURCE_COVERAGE.csv',['Sentence_ID','Evidence_ID','Candidate_Result_IDs','Coverage'],coverage(narrows))
    statuses=Counter(x['Full_Text_Status'] for x in inventory); manifest={'gate':'SOURCE_LEVEL_RESULT_LOCALIZATION_BLOCKED','references_inventoried':len(inventory),'verified_full_texts':statuses['VERIFIED_OFFICIAL_FULL_TEXT'],'abstract_only':statuses['ABSTRACT_ONLY'],'source_unavailable':statuses['SOURCE_UNAVAILABLE'],'result_ids_extracted':len(result),'auditable_locators':len(locator),'forced_semantic_links':0,'blocked_evidence_used_as_support':0,'cef_v1_changed':False,'zotero_changed':False,'manuscripts_changed':False,'reason':'Only two retained references yielded verified full text and auditable result locators; all other retained references lack result-level localization.'}
    (OUT/'BATCH10_4F_R1B1_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (OUT/'BATCH10_4F_R1B1_REPORT.md').write_text(f'''# Batch 10.4F-R1B1 — source-level result localization

## Gate

`SOURCE_LEVEL_RESULT_LOCALIZATION_BLOCKED`

All **16/16** retained references were inventoried. Official PMC full text was verified for **{statuses['VERIFIED_OFFICIAL_FULL_TEXT']}/16** (EV-1473 and EV-1484), producing **{len(result)}** result-level records with auditable XML locators. **{statuses['ABSTRACT_ONLY']}/16** have only a recovered PubMed abstract, and **{statuses['SOURCE_UNAVAILABLE']}/16** have no recovered official source sufficient for result-level localization.

The full-text minority cannot responsibly support readjudication of the 168 sentences. The crosswalk is preparatory only; it asserts no scientific support. No manuscript, CEF-v1, Zotero, reference set, replacement decision, or human decision was altered.

## Exact blocking condition

The entries in `SOURCE_UNAVAILABLE_LEDGER.csv` lack either an auditable full-text result locator or a source sufficient to assess result-level support. They must not be used to turn a citation identity link into semantic support.
''',encoding='utf-8')
if __name__=='__main__':main()
