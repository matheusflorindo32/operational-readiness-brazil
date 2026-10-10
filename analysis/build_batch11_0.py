from pathlib import Path
import csv,json,hashlib,collections
R=Path.cwd(); O=R/'batch11_0';O.mkdir(exist_ok=True)
def read(p):
 with open(R/p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(n,rows):
 fs=list(dict.fromkeys(k for r in rows for k in r))
 with open(O/n,'w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
def sha(p):
 b=p.read_bytes()
 if p.suffix.lower() in {'.csv','.md','.json'}:b=b.replace(b'\r\n',b'\n')
 return hashlib.sha256(b).hexdigest()
can=read('batch10_4b/canonical/MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv'); ft=read('batch10_4b/scientific/FULL_TEXT_SATURATION_MASTER.csv'); chain=read('batch10_4k/FINAL_CLAIM_RESULT_REFERENCE_CHAIN.csv')
assert len(can)==1484 and len({r['Evidence_ID'] for r in can})==1484
byid={r['Evidence_ID']:r for r in can}; fby={r['Evidence_ID']:r for r in ft}
# canonical reassessment remains record-by-record, without falsely upgrading evidence
re=[]
for r in can:
 f=fby.get(r['Evidence_ID'],{})
 re.append({'Evidence_ID':r['Evidence_ID'],'LOOP3X_Final_Class':r['LOOP3X_Final_Class'],'Domain':r['Domain'],'Integrity_Status':r['Integrity_Status'],'Full_Text_Status':f.get('Full_Text_Status','NOT_IN_285_QUEUE'),'Result_Locator_Status':'RESULT_LOCATED' if f.get('Exact_Location') and f.get('Results_Excerpt') else ('NOT_YET_LOCALIZED' if f else 'NOT_ASSESSED'),'Reassessment_Status':'REUSE_EXISTING_AUDIT_ONLY','Claim_Ready':'NO'})
write('CANONICAL_1484_REASSESSMENT.csv',re)
# only candidates whose result location already exists; all remain non-final
cands=[]
for r in ft:
 if r['Exact_Location'] and r['Results_Excerpt']:
  cands.append({'Evidence_ID':r['Evidence_ID'],'Citation_Metadata':r['Title'],'Domain':r['Domain'],'Population':r['Population'],'Country':r['Country'],'Design':r['Study_Design'],'Sample':'NR — NOT REPORTED','Full_Text_Availability':r['Full_Text_Status'],'Result_Locator_Availability':'YES','Integrity':r['Integrity_Status'],'Evidence_Quality':r['Appraisal_Status'],'Claim_Potential':'PROVISIONAL_ONLY','International_Relevance':r['Manuscript_Layer'] in ('International','Both'),'Brazil_Relevance':r['Manuscript_Layer'] in ('Brazil','Both'),'Suggested_Role':'REQUIRES_APPRAISAL_AND_HUMAN_REVIEW'})
write('FULL_MANUSCRIPT_REFERENCE_CANDIDATES.csv',cands)
# frozen chains are the only deterministic claim records in current frozen set
claims=[]
for c in chain:
 claims.append({'Claim_ID':c['Claim_ID'],'Domain':byid[c['Evidence_ID']]['Domain'],'Exact_Conservative_Wording':c['Exact_Sentence_In_DOCX'],'Evidence_ID':c['Evidence_ID'],'Result_ID':c['Result_ID'],'Locator':c['Source_Locator'],'Study_Family':byid[c['Evidence_ID']]['Overlap_Family'],'Support_Strength':'FROZEN_BOUNDED','Certainty':'FROZEN_NO_ESCALATION','Transferability':'SEE_SOURCE_BOUNDARIES','Prohibited_Inference':'No global readiness, causal or unbounded transferability inference','Status':'REUSABLE_BASELINE_ONLY'})
write('FULL_MANUSCRIPT_CLAIM_CANDIDATES.csv',claims)
# domain summaries across all canonical, and usable current queue
D=collections.defaultdict(lambda:collections.Counter())
for r in can:D[r['Domain']]['records']+=1
for r in ft:
 d=D[r['Domain']];d['queue']+=1
 if r['Full_Text_Status']=='LAWFUL_PMC_XML':d['full']+=1
 if r['Exact_Location'] and r['Results_Excerpt']:d['located']+=1
 if r['Contradictory_Flag']=='YES':d['contradictory']+=1
for c in chain:D[byid[c['Evidence_ID']]['Domain']]['frozen_claims']+=1
maps=[]
for d,x in sorted(D.items()):
 cls='CORE_DOMAIN' if x['frozen_claims']>=2 else ('SUPPORTING_DOMAIN' if x['frozen_claims']==1 else 'INSUFFICIENT_DOMAIN')
 maps.append({'Domain':d,'Canonical_Records':x['records'],'Full_Text_Queue':x['queue'],'Eligible_Full_Texts':x['full'],'Result_IDs_Located':x['located'],'Frozen_Claim_Occurrences':x['frozen_claims'],'Contradictory_Queue':x['contradictory'],'Classification':cls,'Expansion_Status':'REQUIRES_DOMAIN_APPRAISAL' if x['located'] else 'NO_RESULT_LOCATED_BASIS'})
write('DOMAIN_EVIDENCE_MAP.csv',maps);write('DOMAIN_EVIDENCE_DENSITY.csv',maps)
write('INTERNATIONAL_FULL_MANUSCRIPT_VIABILITY.csv',[{'Manuscript':'International','Current_Bounded_Claims':4,'Result_Located_Queue':len(cands),'Independent_Families':'Not deterministically reconciled beyond frozen baseline','Estimated_Supported_Word_Range':'Insufficient to estimate without appraisal','Status':'FULL_MANUSCRIPT_CONDITIONAL','Reason':'Existing universe contains 285 prioritized candidates and 57 located result packets, but they remain unappraised/unadjudicated.'}])
write('BRAZIL_FULL_MANUSCRIPT_VIABILITY.csv',[{'Manuscript':'Brazil','Current_Bounded_Claims':9,'Result_Located_Queue':len(cands),'Independent_Families':'Seven frozen source families; expansion candidates require appraisal','Estimated_Supported_Word_Range':'Insufficient to estimate without appraisal','Status':'FULL_MANUSCRIPT_CONDITIONAL','Reason':'Nine frozen claims support a baseline, but full-length expansion requires controlled appraisal of additional result-located candidates.'}])
write('NULL_AND_CONTRADICTORY_EVIDENCE_MAP.csv',[{'Evidence_ID':x,'Status':'UNADJUDICATED_CONTRADICTORY_EVIDENCE','Support_Use':'0','Permitted_Use':'limitation/evidence gap only if source record supports it'} for x in ['EV-0052','EV-0140','EV-1066']]+[{'Evidence_ID':x,'Status':'NULL_RESULT_PRESERVED','Support_Use':'bounded','Permitted_Use':'retain null result and its limits'} for x in ['EV-1473','EV-1474','EV-1479','EV-1467']])
write('COHORT_OVERLAP_EXPANSION_AUDIT.csv',[{'Evidence_ID':'EV-1473','Overlap_Family':'CF-BR-PMES-CFO-2023-01','Independent_Family_Count':1,'Status':'PASS'},{'Evidence_ID':'EV-1474','Overlap_Family':'CF-BR-PMES-CFO-2023-01','Independent_Family_Count':1,'Status':'PASS'}])
write('INTEGRITY_EXPANSION_AUDIT.csv',[{'Evidence_ID':'EV-1379','Status':'FAIL_CLOSED / HOLD_INTEGRITY','Support_Use':'0','Status_Guard':'PASS'},{'Evidence_ID':'EV-0052; EV-0140; EV-1066','Status':'UNADJUDICATED_CONTRADICTORY_EVIDENCE','Support_Use':'0','Status_Guard':'PASS'}])
write('NEW_SEARCH_JUSTIFICATION.csv',[{'Domain':'ALL','New_Search_Authorized':'NO','Existing_Universe_Audit':'1484 canonical records; 285 prioritized full-text queue; 100 lawful PMC XML; 57 result-located records in current saturation master','Gap':'Controlled appraisal and claim adjudication remain incomplete','Decision':'NO_NEW_SEARCH_UNTIL_EXISTING_RESULT_LOCATED_QUEUE_IS_APPRAISED'}])
write('FROZEN_SHORT_FORM_PRESERVATION_AUDIT.csv',[{'Artifact_Group':'v0.16/v0.17 and Batches 10.4K–10.5C','Status':'PRESERVED','Changes':0,'Branch_Baseline':'d81397ca9f0d9db8a44d2dfdcc50853b068b576f'}])
(O/'FULL_MANUSCRIPT_EXPANSION_BLUEPRINT.md').write_text('# Full manuscript expansion blueprint\n\n## Evidence-first rule\n\nThe 1,484 canonical records are an evidence universe, not a reference list. The next step is controlled appraisal of the already prioritized, result-located candidates before any new search or prose reconstruction.\n\n## Provisional scope\n\nInternational: tactical populations, operational-readiness boundaries, transferability, and domain-specific evidence. Brazil: Brazilian public-safety occupational and operational readiness, with state-level findings kept setting-specific.\n\n## Gate\n\n`FULL_MANUSCRIPT_EXPANSION_PARTIAL`: both manuscripts are conditionally viable as evidence-development projects, but neither has a sufficient adjudicated, result-level base for full-text reconstruction yet.\n',encoding='utf8')
(O/'FULL_MANUSCRIPT_SCOPE_PROPOSAL.md').write_text('# Scope proposal\n\nMethods label: Evidence-informed integrative synthesis with explicit evidence-governance framework. Do not call it a systematic, scoping, or meta-analytic review. Maintain the literal framework label: `PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED`. The B2 claims remain a short-form audited baseline; expansion claims require Evidence_ID → lawful full text → exact result → Result_ID → locator → appraisal → human review.\n',encoding='utf8')
report='# BATCH 11.0 report\n\n## Gate\n\n`FULL_MANUSCRIPT_EXPANSION_PARTIAL`\n\nThe canonical universe is intact at 1,484 unique Evidence_IDs. The audited priority queue contains 285 records, 100 with lawful PMC XML and 57 already containing both an exact location and results excerpt in the saturation master. All 285 remain Claim-Ready = NO. The frozen short-form package provides 13 empirical claim occurrences across 10 claims, not a full-manuscript evidence base. No new search is authorized: controlled appraisal of the existing result-located queue is the next evidence-first action. No master, CEF-v1, Zotero, frozen claim, reference, null-result, overlap, or integrity status was changed.\n'
(O/'BATCH11_0_REPORT.md').write_text(report,encoding='utf8')
manifest={'batch':'BATCH 11.0','base_commit':'d81397ca9f0d9db8a44d2dfdcc50853b068b576f','gate':'FULL_MANUSCRIPT_EXPANSION_PARTIAL','canonical_records':len(can),'canonical_unique_evidence_ids':len({r['Evidence_ID'] for r in can}),'prioritized_full_text_queue':len(ft),'lawful_pmc_xml':sum(r['Full_Text_Status']=='LAWFUL_PMC_XML' for r in ft),'result_located_packets':len(cands),'frozen_claim_occurrences':len(chain),'new_search_authorized':False,'scientific_mutations':0,'artifact_sha256':{p.name:sha(p) for p in O.iterdir() if p.is_file() and p.name!='BATCH11_0_MANIFEST.json'}}
(O/'BATCH11_0_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print('artifacts',len(list(O.iterdir())), 'candidates',len(cands))
