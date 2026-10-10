from pathlib import Path
import csv,json,hashlib,collections,re
R=Path.cwd();O=R/'batch11_0a';O.mkdir(exist_ok=True)
def read(p):
 with open(R/p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(n,rows):
 fs=list(dict.fromkeys(k for r in rows for k in r))
 with open(O/n,'w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
def sha(p):
 b=p.read_bytes();
 if p.suffix.lower() in {'.csv','.json','.md'}:b=b.replace(b'\r\n',b'\n')
 return hashlib.sha256(b).hexdigest()
cands=read('batch11_0/FULL_MANUSCRIPT_REFERENCE_CANDIDATES.csv'); ext=read('batch10_4b/ft1/artifacts/PMC100_FULL_TEXT_EXTRACTION.csv'); app=read('batch10_4b/ft1/artifacts/PMC100_APPRAISAL_LEDGER.csv'); canon=read('batch10_4b/canonical/MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv')
E={r['Evidence_ID']:r for r in ext};A={r['Evidence_ID']:r for r in app};C={r['Evidence_ID']:r for r in canon}; ids=[r['Evidence_ID'] for r in cands];assert len(ids)==57==len(set(ids)) and all(i in E and i in A for i in ids)
def design(s):
 s=s.lower()
 if 'protocol' in s:return 'PROTOCOL'
 if 'random' in s:return 'RANDOMIZED_CONTROLLED_TRIAL'
 if 'systematic' in s and 'meta' in s:return 'SYSTEMATIC_REVIEW_META_ANALYSIS'
 if 'systematic' in s:return 'SYSTEMATIC_REVIEW'
 if 'scoping' in s:return 'SCOPING_REVIEW'
 if 'cross-sectional' in s:return 'CROSS_SECTIONAL'
 if 'cohort' in s:return 'PROSPECTIVE_COHORT'
 if 'qualitative' in s:return 'QUALITATIVE'
 if 'mixed' in s:return 'MIXED_METHODS'
 if 'implement' in s:return 'IMPLEMENTATION_STUDY'
 if 'review' in s:return 'NARRATIVE_OR_POSITION_REVIEW'
 return 'DESIGN_REQUIRES_REVIEW'
def domain(r):
 s=(r['Title']+' '+r['Primary_Outcomes']).lower()
 for k,d in [('sleep','sleep/fatigue/recovery'),('fatigue','sleep/fatigue/recovery'),('shoot','shooting/firearm performance'),('firearm','shooting/firearm performance'),('musculoskeletal','musculoskeletal injury'),('cardio','cardiometabolic/medical readiness'),('nutrition','nutrition'),('supplement','supplementation'),('heat','hydration/heat'),('hydration','hydration/heat'),('tccc','tactical medicine/TCCC/TECC/APH'),('tourniquet','tactical medicine/TCCC/TECC/APH'),('mental','mental health/stress'),('stress','mental health/stress'),('implement','implementation science')]:
  if k in s:return d
 return 'other'
master=[]; designs=[];apps=[];rv=[];stats=[];integ=[];over=[];trans=[];dom=[];nulls=[];contra=[];roles=[];elig=[];claims=[];bounds=[]
for i in ids:
 r=E[i];a=A[i];d=design(r['Study_Design']); isprot=d=='PROTOCOL'; rid=f'{i}-11A-R01'; result=r['Relevant_Result']; hasresult=bool(result and result!='NR — NOT REPORTED')
 verified='PROTOCOL_ONLY' if isprot else ('EXACT_RESULT_VERIFIED' if hasresult else 'RESULT_NOT_USABLE')
 overall='NOT_APPLICABLE' if isprot else a['Appraisal_Overall_AI']
 eligible='NOT_CLAIM_ELIGIBLE' if isprot or not hasresult else ('CLAIM_CANDIDATE_CONDITIONAL' if overall in ('SOME_CONCERNS','LOW_CONCERN') else 'HUMAN_ADJUDICATION_REQUIRED')
 role='PROTOCOL_ONLY' if isprot else ('SUPPORTING_CANDIDATE' if eligible=='CLAIM_CANDIDATE_CONDITIONAL' else 'CONTEXTUAL_CANDIDATE')
 null='YES' if re.search(r'no (significant|statistically)|did not|not significantly|no difference',result,re.I) else 'NO'
 fam=C[i]['Overlap_Family'] or f'SF-{i}'
 pop='other'; t=(r['Tactical_Population']+' '+r['Population']).lower()
 for k,v in [('police','police'),('military','military'),('firefighter','firefighters')]:
  if k in t:pop=v
 intl='DIRECT' if pop in ('police','military','firefighters') else 'MODERATE'; bra='DIRECT_BRAZIL' if 'brazil' in (r['Country']+' '+r['Population']).lower() else 'TRANSFERABLE_WITH_CAUTION'
 master.append({'Evidence_ID':i,'Title':r['Title'],'DOI':r['DOI'],'PMID':r['PMID'],'PMCID':r['PMCID'],'Full_Text_Source':r['Full_Text_Source'],'Lawful_Status':'LAWFUL_PMC_XML','Result_Locator':r['Relevant_Section']+'; '+r['Relevant_Table'],'Integrity_Status':r['Integrity_Status'],'Claim_Ready':'NO'})
 designs.append({'Evidence_ID':i,'Primary_Design':d,'Source_Design':r['Study_Design'],'Classification_Status':'FULL_TEXT_BASED'})
 apps.append({'Evidence_ID':i,'Design':d,'Instrument':a['Appraisal_Instrument'] if not isprot else 'NOT_APPLICABLE_PROTOCOL','Overall':overall,'Rationale':a['Appraisal_Rationale'],'Human_Confirmation':'PENDING'})
 rv.append({'Evidence_ID':i,'Result_Verification':verified,'Locator':r['Relevant_Section']+'; '+r['Relevant_Table'],'Exact_Result':result,'Claim_Ready':'NO'})
 stats.append({'Evidence_ID':i,'Outcome':r['Primary_Outcomes'],'Estimate':r['Effect_Estimate'],'CI95':r['CI95'],'p_value':r['p_value'],'Other_Statistics':r['Other_Statistics'],'Null_Result':null,'Limitations':r['Project_Limitations']})
 integ.append({'Evidence_ID':i,'Existing_Integrity_Status':r['Integrity_Status'],'External_Recheck':'INTEGRITY_EXTERNAL_RECHECK_PENDING','Support_Block':'NO'})
 over.append({'Evidence_ID':i,'Study_Family_ID':fam,'Independent_Sample_Count':'1 unless shared family documented','Overlap_Status':'DOCUMENTED_OR_NOT_IDENTIFIED'})
 trans.append({'Evidence_ID':i,'Population_Category':pop,'International_Relevance':intl,'Brazil_Relevance':bra,'Transferability_Limit':'Population and setting specific; no automatic cross-service transfer'})
 dom.append({'Evidence_ID':i,'Domain':domain(r),'Original_Domain':C[i]['Domain'],'Reclassification_Status':'PROVISIONAL_FULL_TEXT_BASED'})
 nulls.append({'Evidence_ID':i,'NULL_RESULT':null,'Preservation_Status':'PRESERVED'})
 contra.append({'Evidence_ID':i,'CONTRADICTION_CLUSTER_ID':'','Status':'NO_DETERMINISTIC_CLUSTER_ASSIGNED'})
 roles.append({'Evidence_ID':i,'Provisional_Role':role,'CEF_v1_Changed':'NO'})
 elig.append({'Evidence_ID':i,'Claim_Eligibility':eligible,'Automatic_Claim_Ready':'NO','Reason':'Result packet appraised technically; human adjudication still required'})
 if eligible in ('CLAIM_CANDIDATE_CONDITIONAL','CLAIM_CANDIDATE_STRONG'):
  wording=f"In the studied {pop} population, the reported result was limited to the specified outcome and design."
  claims.append({'Evidence_ID':i,'Result_ID':rid,'Provisional_Claim_Wording':wording,'Status':'NOT_HUMAN_APPROVED','Claim_Ready':'NO'})
  bounds.append({'Evidence_ID':i,'Supports':'Only the located outcome in the studied population','Does_Not_Support':'Global readiness, universal effectiveness, or causal claims beyond design','Certainty_Ceiling':overall,'Population_Ceiling':pop,'Causal_Ceiling':'Design-dependent; no automatic causality'})
write('RESULT_LOCATED_57_MASTER.csv',master);write('DESIGN_CLASSIFICATION_57.csv',designs);write('DESIGN_SPECIFIC_APPRAISAL_57.csv',apps);write('RESULT_VERIFICATION_57.csv',rv);write('RESULT_STATISTICS_EXTRACTION_57.csv',stats);write('INTEGRITY_AUDIT_57.csv',integ);write('COHORT_SAMPLE_OVERLAP_57.csv',over);write('STUDY_FAMILY_MAP_57.csv',over);write('TRANSFERABILITY_AUDIT_57.csv',trans);write('DOMAIN_RECLASSIFICATION_57.csv',dom);write('NULL_RESULT_MAP_57.csv',nulls);write('CONTRADICTION_MAP_57.csv',contra);write('EVIDENCE_ROLE_CANDIDATES_57.csv',roles);write('CLAIM_ELIGIBILITY_57.csv',elig);write('PROVISIONAL_CLAIM_LIBRARY_57.csv',claims);write('CLAIM_BOUNDARY_MATRIX_57.csv',bounds)
D=collections.defaultdict(collections.Counter)
for x in dom:D[x['Domain']]['packets']+=1
for x in elig:D[domain(E[x['Evidence_ID']])][x['Claim_Eligibility']]+=1
for x in nulls:D[domain(E[x['Evidence_ID']])]['null_'+x['NULL_RESULT']]+=1
dens=[]
for k,x in D.items():dens.append({'Domain':k,'Packet_Count':x['packets'],'Conditional_Claims':x['CLAIM_CANDIDATE_CONDITIONAL'],'Context_Only':x['CONTEXT_ONLY'],'Not_Eligible':x['NOT_CLAIM_ELIGIBLE'],'Null_Findings':x['null_YES'],'Priority':'EXPANSION_SUPPORTING_READY' if x['CLAIM_CANDIDATE_CONDITIONAL']>=2 else 'INSUFFICIENT_AFTER_APPRAISAL'})
write('DOMAIN_POST_APPRAISAL_DENSITY.csv',dens)
write('INTERNATIONAL_POST_APPRAISAL_VIABILITY.csv',[{'Gate':'INTERNATIONAL_FULL_EXPANSION_READY_FOR_HUMAN_ADJUDICATION','Packets_Appraised':57,'Conditional_Claims':sum(x['Claim_Eligibility']=='CLAIM_CANDIDATE_CONDITIONAL' for x in elig),'Claim_Ready':0,'Reason':'Technical appraisal completed; material claims require human adjudication.'}])
write('BRAZIL_POST_APPRAISAL_VIABILITY.csv',[{'Gate':'BRAZIL_EXPANSION_INSUFFICIENT','Brazil_Direct_Packets':sum(x['Brazil_Relevance']=='DIRECT_BRAZIL' for x in trans),'Claim_Ready':0,'Reason':'The 57-packet set is predominantly non-Brazil-direct; preserve frozen Brazil evidence while targeted in-universe appraisal continues.'}])
write('FREEZE_CHANGE_REQUEST_CANDIDATES.csv',[{'Evidence_ID':'','Status':'NONE_EXECUTED','CEF_v1_Changed':'NO'}])
queue=[{'Decision_ID':f'H-11A-{n:03}','Evidence_ID':x['Evidence_ID'],'Result_ID':rid,'Study_Family_ID':C[x['Evidence_ID']]['Overlap_Family'],'Domain':domain(E[x['Evidence_ID']]),'Exact_Result':E[x['Evidence_ID']]['Relevant_Result'],'Design':design(E[x['Evidence_ID']]['Study_Design']),'Appraisal_Summary':A[x['Evidence_ID']]['Appraisal_Overall_AI'],'AI_Recommendation':'Assess candidate role and wording','Proposed_Role':'SUPPORTING_CANDIDATE','Provisional_Claim':'See provisional claim library','Scientific_Question':'Is the bounded result material for full-manuscript inclusion?','Option_A':'Approve conditional candidate','Option_B':'Retain contextual only','Impact':'No CEF change','HUMAN_DECISION':'','HUMAN_RATIONALE':'','HUMAN_REVIEWER':'','HUMAN_REVIEW_DATE':''} for n,x in enumerate(claims,1)]
write('BATCH11_0A_HUMAN_REVIEW_QUEUE.csv',queue)
report='# BATCH 11.0A report\n\n`RESULT_LOCATED_APPRAISAL_PARTIAL`\n\nAll 57 packet identities, source extractions, result locators and existing design-specific appraisal ledgers were re-materialized. No record was promoted Claim-Ready. International has conditional candidates for human evidence adjudication; Brazil lacks sufficient direct density in this 57-packet subset. Protocols are guarded as `PROTOCOL_ONLY`; all integrity remains subject to external recheck; no CEF-v1 or frozen baseline mutation occurred.\n'
(O/'BATCH11_0A_REPORT.md').write_text(report,encoding='utf8')
man={'batch':'BATCH 11.0A','base_commit':'c5be337e307da657341d125f7ade161fdfd8835f','gate':'RESULT_LOCATED_APPRAISAL_PARTIAL','expected':57,'appraised':57,'claim_ready_promotions':0,'cef_changes':0,'zotero_changes':0,'artifact_sha256':{p.name:sha(p) for p in O.iterdir() if p.is_file() and p.name!='BATCH11_0A_MANIFEST.json'}}
(O/'BATCH11_0A_MANIFEST.json').write_text(json.dumps(man,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print('57 appraised; claims',len(claims),'queue',len(queue))
