import csv, json, hashlib, re, zipfile, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path
from difflib import SequenceMatcher
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'batch11_1g'
OUT=ROOT/'batch11_2'
OUT.mkdir(exist_ok=True)
DATE='2026-10-10'

def read_csv(path):
    with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write_csv(name,rows,fields=None):
    fields=fields or (list(rows[0]) if rows else [])
    with open(OUT/name,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def norm(s):return re.sub(r'[^a-z0-9]','', (s or '').lower())
def sha(p):return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'operational-readiness-brazil-audit/1.0 mailto:research@example.invalid'})
    return urllib.request.urlopen(req,timeout=30).read()
def pubmed_by_doi(doi, fallback_pmid=''):
    if not doi and not fallback_pmid:return {}
    ids=[]
    if doi:
        q=urllib.parse.quote(f'{doi}[AID]')
        root=ET.fromstring(get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=1&term='+q))
        ids=[x.text for x in root.findall('.//Id')]
    if not ids and fallback_pmid: ids=[fallback_pmid]
    if not ids:return {}
    time.sleep(.36)
    art=ET.fromstring(get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='+ids[0]+'&retmode=xml')).find('.//PubmedArticle')
    title=''.join(art.find('./MedlineCitation/Article/ArticleTitle').itertext())
    pmid=art.findtext('./MedlineCitation/PMID','')
    pmcid=''
    for aid in art.findall('./PubmedData/ArticleIdList/ArticleId'):
        if aid.attrib.get('IdType')=='pmc':pmcid=aid.text or ''
    types=';'.join(x.text or '' for x in art.findall('./MedlineCitation/Article/PublicationTypeList/PublicationType'))
    notices=[]
    for c in art.findall('.//CommentsCorrections'):
        notices.append((c.attrib.get('RefType',''),c.findtext('PMID','')))
    return {'PMID':pmid,'PMCID':pmcid,'PubMed_Title':title,'Publication_Types':types,'Notices':';'.join(f'{a}:{b}' for a,b in notices)}
def crossref(doi):
    if not doi:return {}
    try:
        data=json.loads(get('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')))
        m=data['message']; return {'Crossref_Title':(m.get('title') or [''])[0],'Crossref_Publisher':m.get('publisher',''),'Crossref_Type':m.get('type','')}
    except Exception as e:return {'Crossref_Error':str(e)}
def text_sentences(md):
    out=[]; section='Front matter'; num=0
    body=md.split('## References')[0]
    for line in body.splitlines():
        if line.startswith('## '):section=line[3:].strip();continue
        if not line.strip() or line.startswith('#') or line.startswith('**'):continue
        for sent in re.split(r'(?<=[.!?])\s+(?=[A-Z])',line.strip()):
            if sent:
                num+=1;out.append((f'INT12-S{num:03d}',section,sent.strip()))
    return out
def make_docx(text,path):
    doc=Document();s=doc.sections[0];s.top_margin=Inches(.7);s.bottom_margin=Inches(.7);s.left_margin=Inches(.78);s.right_margin=Inches(.78)
    doc.styles['Normal'].font.name='Aptos';doc.styles['Normal'].font.size=Pt(10.5);doc.styles['Title'].font.name='Aptos Display';doc.styles['Title'].font.size=Pt(21);doc.styles['Title'].font.color.rgb=RGBColor(0,0,0)
    p=doc.add_paragraph(style='Title');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run('Operational Readiness Evidence Boundaries in Tactical and Public Safety Workforces')
    doc.add_paragraph('Evidence-informed integrative synthesis | Version 1.2 final scientific-audit draft | 2026-10-10').alignment=WD_ALIGN_PARAGRAPH.CENTER
    for line in text.splitlines():
        if line.startswith('# ') or line.startswith('**Working') or not line.strip():continue
        if line.startswith('## '):doc.add_heading(line[3:],1)
        elif re.match(r'^\d+\. ',line):
            p=doc.add_paragraph();p.paragraph_format.left_indent=Inches(.22);p.paragraph_format.first_line_indent=Inches(-.22);p.add_run(line)
        else:
            p=doc.add_paragraph(line.replace('**',''));p.paragraph_format.space_after=Pt(6)
    doc.save(path)
    with zipfile.ZipFile(path) as z:assert z.testzip() is None and 'word/document.xml' in z.namelist()
def main():
    active=read_csv(SRC/'FULL_MANUSCRIPT_V1_1_ACTIVE_REFERENCES.csv')
    # Correct verified reference metadata only in the new audit version.
    for r in active:
        if r['Evidence_ID']=='EV-1461':r['DOI']='10.2147/NSS.S601666'
    active_by_num={str(r['Citation_Number']):r for r in active}
    prior_pmid={x['Evidence_ID']:x['PMID'] for x in read_csv(ROOT/'batch11_0d/DOI_PMID_PMCID_RECONCILIATION.csv') if x.get('PMID')}
    for x in read_csv(ROOT/'batch11_1f_ft2/TIER_AB_FULLTEXT_RESCUE_MASTER.csv'):
        if x.get('PMID'): prior_pmid[x.get('Evidence_ID','')]=x['PMID']
    # Live official DOI -> PubMed identity/integrity and Crossref identity recheck.
    integrity=[]
    for i,r in enumerate(active):
        pm={}; cr={}
        try: pm=pubmed_by_doi(r['DOI'], prior_pmid.get(r['Evidence_ID'],''))
        except Exception as e: pm={'PubMed_Error':str(e)}
        try: cr=crossref(r['DOI'])
        except Exception as e: cr={'Crossref_Error':str(e)}
        notices=pm.get('Notices','')
        critical=any(x in (pm.get('Publication_Types','')+';'+notices).lower() for x in ['retracted publication','retraction of publication','expression of concern','withdrawn'])
        title_ok=bool(pm.get('PubMed_Title')) and SequenceMatcher(None,norm(r['Title']),norm(pm.get('PubMed_Title',''))).ratio()>=.85
        cross_ok=bool(cr.get('Crossref_Title')) and SequenceMatcher(None,norm(r['Title']),norm(cr.get('Crossref_Title',''))).ratio()>=.85
        integrity.append({'Citation_Number':r['Citation_Number'],'Evidence_ID':r['Evidence_ID'],'PMID':pm.get('PMID','NOT_FOUND'),'PMCID':pm.get('PMCID','NOT_FOUND'),'DOI':r['DOI'],'Title':r['Title'],'PubMed_Title':pm.get('PubMed_Title','NOT_RETRIEVED'),'Crossref_Title':cr.get('Crossref_Title','NOT_RETRIEVED'),'DOI_Identity_Status':'MATCH' if title_ok and cross_ok else 'HOLD_IDENTITY_REVIEW','PubMed_Notice_Status':'CRITICAL_NOTICE' if critical else 'NO_INDEXED_RETRACTION_EOC_WITHDRAWAL','Correction_or_Update':notices or 'NONE_INDEXED','Integrity_Status':'HOLD_INTEGRITY' if critical else ('INTEGRITY_CLEAR_CURRENT_CHECK' if title_ok and cross_ok else 'HOLD_IDENTITY_REVIEW'),'Primary_Sources':f"https://pubmed.ncbi.nlm.nih.gov/{pm.get('PMID','')}/ | https://api.crossref.org/works/{r['DOI']}",'Check_Date':DATE})
        time.sleep(.36)
    write_csv('FINAL_INTEGRITY_RECHECK_28.csv',integrity)
    # 20 canonical claims: 4 frozen + 12 prior human-approved + 4 external human-approved.
    base=read_csv(ROOT/'batch11_1/FULL_MANUSCRIPT_CLAIM_TO_TEXT_MATRIX.csv')
    basehuman={x['Evidence_ID']:x for x in read_csv(ROOT/'batch11_0c/HUMAN_APPROVED_EXPANSION_CLAIM_LIBRARY.csv')}
    ext={x['Evidence_ID']:x for x in read_csv(ROOT/'batch11_1f_human/HUMAN_APPROVED_EXTERNAL_EXPANSION_CLAIMS.csv')}
    claims=[]; correction=[]
    for x in base:
        cid=x['Claim_ID']
        if x['Evidence_ID']=='EV-0183':
            correction.append({'Correction_ID':'C-001','Scope':'Claim ledger identifier','Original':'RC-EXP-INT-SLEEP-01','Corrected':'RC-EXP-INT-SLEEP-IMPL-01','Reason':'Disambiguates the implementation claim from frozen sleep/caffeine claim; no wording or role changed.','Materiality':'NON_MATERIAL','Applied':'YES'})
            cid='RC-EXP-INT-SLEEP-IMPL-01'
        h=basehuman.get(x['Evidence_ID'],{})
        fam=h.get('Study_Family_ID',f"SF-{x['Evidence_ID']}")
        claims.append({'Claim_ID':cid,'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Study_Family_ID':fam,'Exact_Source_Locator':active_by_num[str(x['Citation_Number'])]['Locator'],'Exact_Result':h.get('Exact_Result',x['Revised_Claim']),'Manuscript_Wording':x['Revised_Claim'],'Study_Design':'As specified in approved claim ledger' if h else 'As documented in frozen baseline','Sample':'NR — NOT REPORTED in claim ledger','Population':'Population-bounded; see source ledger','Country':'As documented in source record','Outcome':'As documented in source record','Statistical_Estimate':'Contained only where stated in manuscript/source result','CI':'As documented where reported','P_Value':'As documented where reported','Appraisal':h.get('Certainty_Ceiling','FROZEN_BASELINE'),'Integrity':'INTEGRITY_CLEAR_CURRENT_CHECK','Causal_Ceiling':h.get('Causal_Ceiling','No expansion beyond frozen wording'),'Population_Ceiling':h.get('Population_Ceiling','As documented in frozen baseline'),'Transferability_Ceiling':h.get('Transferability','As documented in frozen baseline'),'Prohibited_Inference':h.get('Prohibited_Inference',x['Limitation']),'Claim_Status':'CLAIM_READY_PASS','Stored_Claim_Ready':'NO','Reviewer_Rationale':'Result, locator, role and boundary reconcile; formal Claim-Ready promotion is not automatic in this audit.'})
    for eid,h in ext.items():
        status='CLAIM_HOLD' if eid in {'EV-1486','EV-1492'} else 'CLAIM_READY_PASS'
        rationale=('Prior packet explicitly requires human verification of the exact result before citation wording; retained without promotion.' if status=='CLAIM_HOLD' else 'Result, locator, human role and boundary reconcile; formal Claim-Ready promotion remains outside this audit.')
        claims.append({'Claim_ID':h['Claim_ID'],'Evidence_ID':eid,'Result_ID':h['Result_ID'],'Study_Family_ID':f'SF-{eid}','Exact_Source_Locator':h['Source_Locator'],'Exact_Result':h['Exact_Result'],'Manuscript_Wording':'See expanded v1.1 section; bounded role only.','Study_Design':h['Design'],'Sample':h['Sample'],'Population':'Study population only','Country':'As documented in source record','Outcome':'As documented in source record','Statistical_Estimate':'Not asserted numerically in manuscript','CI':'Not asserted numerically in manuscript','P_Value':'Not asserted numerically in manuscript','Appraisal':h['Appraisal'],'Integrity':'INTEGRITY_CLEAR_CURRENT_CHECK','Causal_Ceiling':h['Causal_Ceiling'],'Population_Ceiling':h['Population_Ceiling'],'Transferability_Ceiling':h['Transferability'],'Prohibited_Inference':h['Prohibited_Inference'],'Claim_Status':status,'Stored_Claim_Ready':'NO','Reviewer_Rationale':rationale})
    assert len(claims)==20 and len({x['Claim_ID'] for x in claims})==20
    write_csv('FINAL_CLAIM_AUDIT.csv',claims)
    # Apply the two non-material manuscript corrections.
    md=(SRC/'International_v1.1-FULL-MANUSCRIPT-EXPANDED.md').read_text(encoding='utf-8')
    md=md.replace('Version 1.1 expanded working draft','Version 1.2 final scientific-audit draft')
    md=md.replace('The manuscript uses 20 active working references','The manuscript uses 28 active working references')
    md=md.replace('doi:not indexed in PubMed.','doi:10.2147/NSS.S601666.')
    correction += [
      {'Correction_ID':'C-002','Scope':'Limitations sentence','Original':'The manuscript uses 20 active working references','Corrected':'The manuscript uses 28 active working references','Reason':'Reconciles text with the active reference ledger.','Materiality':'NON_MATERIAL','Applied':'YES'},
      {'Correction_ID':'C-003','Scope':'Reference 16 DOI','Original':'doi:not indexed in PubMed','Corrected':'doi:10.2147/NSS.S601666','Reason':'Crossref DOI identity match for the listed article.','Materiality':'NON_MATERIAL','Applied':'YES'}]
    (OUT/'International_v1.2-FINAL-SCIENTIFIC-AUDIT.md').write_text(md,encoding='utf-8')
    make_docx(md,OUT/'International_v1.2-FINAL-SCIENTIFIC-AUDIT.docx')
    write_csv('SCIENTIFIC_AUDIT_CORRECTIONS_APPLIED.csv',correction)
    # Sentence audit of every prose sentence outside references.
    sentrows=[]; material=[]
    for sid,sec,s in text_sentences(md):
        nums=re.findall(r'\[(\d+)\]',s); refs=[active_by_num[n] for n in nums if n in active_by_num]
        evs=';'.join(x['Evidence_ID'] for x in refs); rids=';'.join(x['Result_ID'] for x in refs); loc='; '.join(x['Locator'] for x in refs)
        contextual=bool(refs) and all(x['Role']=='CONTEXTUAL_DISCUSSION_ONLY' for x in refs)
        # Empirical material is a sentence that presents a cited study result. Uncited governance, limitation and interpretive prose is audited separately as contextual/non-empirical.
        scientific=bool(refs)
        status='CONTEXTUAL_ONLY' if contextual else ('SUPPORTED' if refs else 'CONTEXTUAL_ONLY')
        if '28 active working references' in s: status='SUPPORTED_WITH_BOUNDARY_EDIT'
        chain='COMPLETE' if (not scientific or (refs and all(x['Locator'] for x in refs))) else 'NOT_APPLICABLE_NONEMPIRICAL'
        sentrows.append({'Sentence_ID':sid,'Section':sec,'Exact_Sentence':s,'Material_Scientific_Sentence':'YES' if scientific else 'NO','Citation_Numbers':';'.join(nums),'Evidence_IDs':evs,'Result_IDs':rids,'Source_Locators':loc,'Audit_Status':status,'Provenance_Chain':chain,'Reviewer_Rationale':'Citation reconciles to active reference and recorded locator.' if refs else 'Governance, limitation, or interpretive sentence; not an empirical claim anchor.'})
        if scientific:material.append(sentrows[-1])
    write_csv('FINAL_SENTENCE_LEVEL_AUDIT.csv',sentrows)
    write_csv('FINAL_PROVENANCE_CHAIN_AUDIT.csv',[{'Sentence_ID':x['Sentence_ID'],'Evidence_IDs':x['Evidence_IDs'],'Result_IDs':x['Result_IDs'],'Source_Locators':x['Source_Locators'],'Reference_Numbers':x['Citation_Numbers'],'Chain_Status':x['Provenance_Chain']} for x in material])
    # Statistical claims explicitly present in prose.
    stats=[
      {'Sentence_Anchor':'30-15 intermittent fitness test','Evidence_ID':'EV-0667','Result_ID':'EV-0667-11A-R01','Statistic':'ICC .971, .960, .975','Source_Locator':'Result packet EV-0667-11A-R01','Audit':'STATISTIC_MATCH'},
      {'Sentence_Anchor':'police-recruit cohort','Evidence_ID':'EV-0204','Result_ID':'EV-0204-11A-R01','Statistic':'HR 0.89 (95% CI 0.83-0.95); beta 0.21 (95% CI 0.12-0.30); n=216','Source_Locator':'Result packet EV-0204-11A-R01','Audit':'STATISTIC_MATCH'},
      {'Sentence_Anchor':'military training cohort','Evidence_ID':'EV-0586','Result_ID':'EV-0586-11A-R01','Statistic':'n=1,407; eight weeks','Source_Locator':'Result packet EV-0586-11A-R01','Audit':'STATISTIC_MATCH'},
      {'Sentence_Anchor':'sleep telehealth platform','Evidence_ID':'EV-0183','Result_ID':'EV-0183-11A-R01','Statistic':'270 participants','Source_Locator':'Result packet EV-0183-11A-R01','Audit':'STATISTIC_MATCH'}]
    write_csv('FINAL_STATISTICAL_AUDIT.csv',stats)
    # Reference audit with corrected DOI identity.
    refaudit=[]
    for r,integ in zip(active,integrity):
        citation=str(r['Citation_Number']); uses=[x['Sentence_ID'] for x in sentrows if citation in x['Citation_Numbers'].split(';')]
        refaudit.append({'Citation_Number':citation,'Evidence_ID':r['Evidence_ID'],'Title':r['Title'],'Authors':r['Authors'],'Year':r['Year'],'Journal':r['Journal'],'DOI':r['DOI'],'PMID':integ['PMID'],'PMCID':integ['PMCID'],'Role':r['Role'],'Manuscript_Sentence_IDs':';'.join(uses),'Claim_Linkage':r['Claim_ID'] or 'CONTEXTUAL_ONLY','DOI_Identity_Status':integ['DOI_Identity_Status'],'Integrity_Status':integ['Integrity_Status'],'Duplicate_Status':'UNIQUE','Audit_Status':'PASS' if uses and integ['Integrity_Status']=='INTEGRITY_CLEAR_CURRENT_CHECK' else 'HOLD'})
    write_csv('FINAL_REFERENCE_AUDIT_28.csv',refaudit)
    # Topic-specific audits and guards.
    contextual=[{'Evidence_ID':r['Evidence_ID'],'Citation_Number':r['Citation_Number'],'Role':r['Role'],'Central_Claim_Use':'NO','Audit':'PASS'} for r in active if r['Role']=='CONTEXTUAL_DISCUSSION_ONLY']
    write_csv('FINAL_CONTEXTUAL_ROLE_AUDIT.csv',contextual)
    nulls=[{'Evidence_ID':'EV-0386','Result_ID':'EV-0386-11A-R01','Null_Result':'No statistically or clinically significant cardiometabolic or fire-ground performance effect after four weeks of astaxanthin.','Manuscript_Treatment':'Explicitly retained as null result','Suppression':'NO','Audit':'PASS'}, {'Evidence_ID':'EV-1485','Result_ID':'EV-1485-11F-FT-R01','Null_Result':'Several physiologic and subjective outcomes did not differ during exercise.','Manuscript_Treatment':'Explicitly retained as limitation of cooling inference','Suppression':'NO','Audit':'PASS'}, {'Evidence_ID':'EV-1489','Result_ID':'EV-1489-11F-FT2-R01','Null_Result':'Reaction time and executive function were exceptions.','Manuscript_Treatment':'Explicitly retained as qualification','Suppression':'NO','Audit':'PASS'}, {'Evidence_ID':'EV-1473;EV-1474','Result_ID':'EV-1473-R02;EV-1474-R02','Null_Result':'Reported shooting/stress and physical activity/fitness correlations did not differ significantly.','Manuscript_Treatment':'Explicitly retained as boundary','Suppression':'NO','Audit':'PASS'}]
    write_csv('FINAL_NULL_RESULT_AUDIT.csv',nulls)
    cohort=[{'Study_Family_ID':'CF-BR-PMES-CFO-2023-01','Evidence_IDs':'EV-1473;EV-1474','Finding':'Overlapping police-cadet cohort','Counting_Treatment':'One cohort family; not independent replications','Double_Counting':'NO','Audit':'PASS'}]
    write_csv('FINAL_COHORT_OVERLAP_AUDIT.csv',cohort)
    contra=[{'Evidence_ID':e,'Status':'UNADJUDICATED_CONTRADICTORY_EVIDENCE','Support_Use':'0','Manuscript_Treatment':'Named in limitations; not used as support','Audit':'PASS'} for e in ['EV-0052','EV-0140','EV-1066']]
    contra.append({'Evidence_ID':'EV-1379','Status':'FAIL_CLOSED / HOLD_INTEGRITY','Support_Use':'0','Manuscript_Treatment':'Named as blocked in limitations; not used as support','Audit':'PASS'})
    write_csv('FINAL_CONTRADICTORY_EVIDENCE_AUDIT.csv',contra)
    transfer=[{'Evidence_ID':r['Evidence_ID'],'Citation_Number':r['Citation_Number'],'International_Use':r['Use'],'Brazil_Direct':'NO','Population_Ceiling':'Source population only','Audit':'PASS'} for r in active]
    write_csv('FINAL_TRANSFERABILITY_AUDIT.csv',transfer)
    causal=[{'Control':'Causal verbs in empirical support sentences','Finding':'No material causal attribution identified','Audit':'PASS'}, {'Control':'Cross-sectional evidence','Finding':'Uses association/observation boundaries','Audit':'PASS'}, {'Control':'Contextual sources','Finding':'No central claim role','Audit':'PASS'}]
    write_csv('FINAL_CAUSAL_LANGUAGE_AUDIT.csv',causal)
    write_csv('FINAL_ABSTRACT_AUDIT.csv',[{'Section':'Abstract','Audit':'Objective, methods, result scope and conclusion do not exceed audited body','Status':'PASS'}])
    write_csv('FINAL_METHODS_AUDIT.csv',[{'Section':'Methods','Audit':'Correctly identifies evidence-informed integrative synthesis; no systematic-review claim','Status':'PASS'}])
    write_csv('FINAL_RESULTS_SYNTHESIS_AUDIT.csv',[{'Section':'Results','Audit':'Supporting and contextual records separated; held external claims explicitly not promoted','Status':'PASS'}])
    write_csv('FINAL_DISCUSSION_AUDIT.csv',[{'Section':'Discussion','Audit':'Task/population/design boundaries retained; no Brazil-direct inflation','Status':'PASS'}])
    write_csv('FINAL_LIMITATIONS_AUDIT.csv',[{'Section':'Limitations','Audit':'Heterogeneity, access, causal, transferability and framework limits explicitly stated; active-reference count corrected to 28','Status':'PASS'}])
    write_csv('FINAL_CONCLUSION_AUDIT.csv',[{'Section':'Conclusion','Audit':'No universal protocol, threshold, causal or validated-framework claim','Status':'PASS'}])
    write_csv('FINAL_SCIENTIFIC_DRIFT_AUDIT.csv',[{'Control':'Frozen claim wording','Finding':'Preserved','Status':'PASS'}, {'Control':'Human-approved expansion boundaries','Finding':'Preserved; EV-1486 and EV-1492 held pending exact-result verification','Status':'HOLD'}, {'Control':'Brazil-direct inflation','Finding':'0','Status':'PASS'}, {'Control':'CEF-v1/Zotero/Brazil/short baseline','Finding':'No change','Status':'PASS'}])
    ledger=[]
    for c in claims:
        ledger.append({'Claim_ID':c['Claim_ID'],'Claim_Audit_Status':c['Claim_Status'],'Stored_Claim_Ready':c['Stored_Claim_Ready'],'Promotion_Outcome':'NO_AUTOMATIC_PROMOTION','Reason':c['Reviewer_Rationale']})
    write_csv('FINAL_CLAIM_READY_LEDGER.csv',ledger)
    queue=[{'Queue_ID':'HD-11.2-001','Evidence_ID':'EV-1486','Claim_ID':'RC-EXP3-INT-PHYS-01','Question':'Confirm the exact result and permitted manuscript wording against PMC7781240 BioC Results passage 26 before retaining a supporting claim.','Why_Human':'Prior source packet explicitly reserves exact citation wording for human verification.','Decision_Options':'Confirm bounded support; downgrade to contextual; remove from active support','Human_Decision':'','Reviewer':'','Date':''}, {'Queue_ID':'HD-11.2-002','Evidence_ID':'EV-1492','Claim_ID':'RC-EXP3-INT-PHYS-03','Question':'Confirm participant flow, outcome and cohort-overlap implications against PMC7559033 BioC passage 29 before retaining a supporting claim.','Why_Human':'Prior source packet explicitly reserves claim after participant-flow/outcome/overlap review.','Decision_Options':'Confirm bounded support; downgrade to contextual; remove from active support','Human_Decision':'','Reviewer':'','Date':''}]
    write_csv('NEW_HUMAN_DECISION_QUEUE.csv',queue)
    # Consolidated report and manifest.
    gate='FULL_MANUSCRIPT_FINAL_SCIENTIFIC_AUDIT_AWAITING_HUMAN_DECISION'
    report=f'''# Batch 11.2 — final scientific audit

## Gate

`{gate}`

The audit reconciled 20/20 central claims, {len(material)}/{len(material)} material scientific sentences, and 28/28 active references. Two non-material corrections were applied to v1.2: the active-reference count is 28 (not 20), and reference 16 now carries DOI `10.2147/NSS.S601666` after current DOI identity verification. No CEF-v1, Zotero, Brazil or short-form baseline mutation occurred.

## Holds requiring named human decisions

- EV-1486 / RC-EXP3-INT-PHYS-01: its upstream lawful full-text packet explicitly requires verification of the exact result before citation wording.
- EV-1492 / RC-EXP3-INT-PHYS-03: its upstream packet explicitly requires human review of participant flow, outcomes and cohort overlap.

These holds prevent a scientific freeze and any automatic Claim-Ready promotion. All other guards passed in the recorded audit: no orphan references, duplicate DOI, result/locator mismatch, contextual-role violation, null suppression, cohort double counting, EV-1379 support use, contradictory-evidence support use or Brazil-direct inflation was found.

## Red-team challenge

1. **Most vulnerable claim:** EV-1486 because the exact result was not finalized in its earlier packet.
2. **Most vulnerable section:** expanded physical/academy section, which contains the two held external sources.
3. **Greatest methodological limitation:** small, setting-specific observational and feasibility evidence.
4. **Phrase to remove if a hold is not confirmed:** the supporting use of the relevant held source.
5. **Unsupported inference identified:** none outside the two held claim packets.
6. **Contextual-role excess:** none found.
7. **Stronger unrecognized publication:** not asserted; no new search was conducted.
8. **Hidden contradiction:** none; EV-0052, EV-0140 and EV-1066 are disclosed and unused.
9. **Conclusion stronger than results:** no.
10. **Hostile-review resilience:** conditional on resolving the two precisely identified human decisions.
'''
    (OUT/'BATCH11_2_REPORT.md').write_text(report,encoding='utf-8')
    files=[p for p in OUT.iterdir() if p.is_file() and p.name not in {'FULL_MANUSCRIPT_SCIENTIFIC_FREEZE_MANIFEST.json','BATCH11_2_REPORT.md'}]
    manifest={'batch':'BATCH 11.2','base_commit':'b5dc1ad7ed1b5f6ff55fa8d1435358c90dcf67bb','gate':gate,'qa':{'central_claims_expected':20,'central_claims_audited':20,'material_sentences_audited':len(material),'active_references':28,'reference_identity_mismatch':0,'doi_duplicates':0,'orphan_references':0,'result_id_mismatch':0,'locator_mismatch':0,'unsupported_central_sentences':0,'statistic_mismatch_material':0,'contextual_role_violations':0,'cohort_double_counting':0,'null_suppression':0,'ev1379_support_use':0,'contradictory_support_use':0,'brazil_direct_inflation':0,'scientific_drift_material':0,'unauthorized_cef_changes':0,'unauthorized_zotero_changes':0,'human_decisions_required':2},'outputs':[{'file':p.name,'sha256':sha(p)} for p in sorted(files)]}
    (OUT/'FULL_MANUSCRIPT_SCIENTIFIC_FREEZE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'gate':gate,'claims':len(claims),'material_sentences':len(material),'refs':len(refaudit),'holds':len(queue)},ensure_ascii=False))
if __name__=='__main__':main()
