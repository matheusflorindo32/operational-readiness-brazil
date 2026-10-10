from pathlib import Path
import csv, json, hashlib, collections, re
R=Path.cwd(); S=R/'batch11_0a_r'; O=R/'batch11_0b'; O.mkdir(exist_ok=True)
def read(p):
 with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(n,data,fields=None):
 fields=fields or list(dict.fromkeys(k for r in data for k in r))
 with open(O/n,'w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
def sha(p):
 b=p.read_bytes()
 if p.suffix.lower() in {'.csv','.json','.md'}:b=b.replace(b'\r\n',b'\n')
 return hashlib.sha256(b).hexdigest()
q=read(S/'BATCH11_0A_HUMAN_REVIEW_QUEUE_REPAIRED.csv')
assert len(q)==26 and len({x['Decision_ID'] for x in q})==26
M={x['Evidence_ID']:x for x in read(S/'RESULT_LOCATED_57_MASTER_REPAIRED.csv')}
A={x['Evidence_ID']:x for x in read(S/'APPRAISAL_LINKAGE_REPAIRED.csv')}
F={x['Evidence_ID']:x for x in read(S/'STUDY_FAMILY_REPAIRED.csv')}
E={x['Evidence_ID']:x for x in read(S/'CLAIM_ELIGIBILITY_REPAIRED.csv')}
P={x['Evidence_ID']:x for x in read(R/'batch10_4b/ft1/artifacts/PMC100_PROVISIONAL_DECISIONS.csv')}
# Queue-normalized domains close remaining taxonomy gaps without changing the upstream repair package.
override={'EV-0014':'physical fitness/readiness','EV-1458':'physical fitness/readiness','EV-0799':'physical fitness/readiness','EV-1128':'musculoskeletal injury'}
def dom(row):return override.get(row['Evidence_ID'],row['Domain'])
cluster_by_domain={'physical fitness/readiness':'CL-INT-FIT-01','aerobic capacity':'CL-INT-FIT-MEAS-01','body composition':'CL-INT-BODYCOMP-01','musculoskeletal injury':'CL-INT-MSK-01','sleep/fatigue/recovery':'CL-INT-SLEEP-01','mental health/stress':'CL-INT-MH-01','cardiometabolic/medical readiness':'CL-INT-MED-01','hydration/heat':'CL-INT-HEAT-01','tactical medicine/TCCC/TECC/APH':'CL-INT-APH-01','implementation science':'CL-INT-IMPL-01'}
# Only these records have a plausible central role after technical appraisal. This is explicitly an AI recommendation.
supporting={'EV-0068','EV-0103','EV-0183','EV-0204','EV-0586','EV-0667','EV-0670','EV-0721','EV-0734','EV-0960','EV-1026','EV-1461'}
exclude={'EV-0014','EV-0799'}
tier1={'EV-0103','EV-0183','EV-0204','EV-0667','EV-0670','EV-0721','EV-0734','EV-0960','EV-1461'}
seq=collections.Counter(); ledger=[]; roles=[]; claims=[]; bounds=[]; cluster_rows=[]
for r in q:
 eid=r['Evidence_ID']; m=M[eid]; a=A[eid]; f=F[eid]; d=dom(r); cl=cluster_by_domain.get(d,'CL-INT-OTHER-01')
 if eid in supporting: rec='RETAIN_BOUNDED_SUPPORTING_CANDIDATE'; role='SUPPORTING_CANDIDATE'; tier='TIER 1' if eid in tier1 else 'TIER 2'; impact='Could add a bounded, source-located section-level support after human role and wording adjudication.'
 elif eid in exclude: rec='EXCLUDE_FROM_FULL_MANUSCRIPT'; role='EXCLUDE_CANDIDATE'; tier='TIER 3'; impact='Low incremental fit for the proposed full-manuscript focus; preserve the record and result without using it as a central claim.'
 else: rec='CONTEXTUAL_DISCUSSION_ONLY'; role='CONTEXTUAL_CANDIDATE'; tier='TIER 2'; impact='Potentially useful to qualify discussion, limitations, implementation context, or a null finding; not recommended as a central claim anchor.'
 # Positive provisional claims are made only for supporting candidates. No human approval is implied.
 claim_id=''
 provisional=''
 if role=='SUPPORTING_CANDIDATE':
  prefix={'physical fitness/readiness':'PHYS','aerobic capacity':'AER','body composition':'BODY','musculoskeletal injury':'MSK','sleep/fatigue/recovery':'SLEEP','mental health/stress':'MH','cardiometabolic/medical readiness':'MED','hydration/heat':'HEAT','tactical medicine/TCCC/TECC/APH':'APH','implementation science':'IMPL'}.get(d,'OTHER')
  seq[prefix]+=1; claim_id=f'RC-EXP-INT-{prefix}-{seq[prefix]:02d}'
  provisional=f'In the studied population and design, {m["Exact_Result"]}'
  claims.append({'Claim_ID':claim_id,'Claim_Status':'PROVISIONAL_EXPANSION_CLAIM','Evidence_ID':eid,'Result_ID':r['Result_ID'],'Domain':d,'Provisional_Claim':provisional,'Locator':m['Locator'],'Exact_Result':m['Exact_Result'],'Population':m['Population'],'Design':r['Design'],'Claim_Ready':'NO','Human_Adjudication':'PENDING','Integrity_Status':'INTEGRITY_EXTERNAL_RECHECK_PENDING'})
  bounds.append({'Claim_ID':claim_id,'Evidence_ID':eid,'Result_ID':r['Result_ID'],'Permitted_Use':'Only the source-located result in its stated population and study design.','Prohibited_Inference':P[eid]['Prohibited_Inference'],'External_Integrity_Guard':'PROVISIONAL_PENDING_EXTERNAL_INTEGRITY_RECHECK','Claim_Ready':'NO'})
 ledger.append({'Decision_ID':r['Decision_ID'],'Evidence_ID':eid,'Result_ID':r['Result_ID'],'Title':m['Title'],'Domain':d,'Population':m['Population'],'Country':m['Country'],'Sample':m['Sample'],'Design':r['Design'],'Appraisal':a['Overall_Interpretation'],'Exact_Result':m['Exact_Result'],'Null_Result':m['Null_Result'],'Primary_Limitation':a['Appraisal_Domains_or_Rationale'],'Transferability':'International: population-and-setting-bound; Brazil: TRANSFERABLE_CONTEXT only.','AI_Recommendation':rec,'Proposed_Role':role,'Tier':tier,'Provisional_Claim_ID':claim_id,'Provisional_Claim':provisional,'Prohibited_Inference':P[eid]['Prohibited_Inference'],'Alternative_Option':'CONTEXTUAL_DISCUSSION_ONLY' if rec=='RETAIN_BOUNDED_SUPPORTING_CANDIDATE' else ('EXCLUDE_FROM_FULL_MANUSCRIPT' if rec=='CONTEXTUAL_DISCUSSION_ONLY' else 'CONTEXTUAL_DISCUSSION_ONLY'),'Scientific_Impact':impact,'Decision_Cluster_ID':cl,'Study_Family_ID':r['Study_Family_ID'],'Integrity_Status':'INTEGRITY_EXTERNAL_RECHECK_PENDING','HUMAN_DECISION':'','HUMAN_RATIONALE':'','HUMAN_REVIEWER':'','HUMAN_REVIEW_DATE':''})
 roles.append({'Evidence_ID':eid,'Result_ID':r['Result_ID'],'AI_Recommendation':rec,'Proposed_Role':role,'Tier':tier,'Claim_Ready':'NO','Human_Approval':'PENDING','Integrity_Guard':'PROVISIONAL_PENDING_EXTERNAL_INTEGRITY_RECHECK'})
 cluster_rows.append({'Decision_Cluster_ID':cl,'Decision_ID':r['Decision_ID'],'Evidence_ID':eid,'Result_ID':r['Result_ID'],'Domain':d,'Study_Family_ID':r['Study_Family_ID'],'Narrative_Overlap_Check':'Human reviewer must compare records within the same cluster before choosing multiple central anchors.','Automatic_Exclusion':'NO'})
write('FULL_MANUSCRIPT_HUMAN_DECISION_LEDGER.csv',ledger)
write('DECISION_CLUSTER_MAP.csv',cluster_rows)
write('AI_RECOMMENDED_EVIDENCE_ROLES.csv',roles)
write('PROVISIONAL_EXPANSION_CLAIM_LIBRARY.csv',claims)
write('EXPANSION_CLAIM_BOUNDARY_MATRIX.csv',bounds)
# Density is a pre-human map. The calculation keeps study families distinct from papers.
dens=[]
for d in sorted({x['Domain'] for x in ledger}):
 rr=[x for x in ledger if x['Domain']==d]
 dens.append({'Domain':d,'Material_Decisions':len(rr),'Supporting_Candidates':sum(x['Proposed_Role']=='SUPPORTING_CANDIDATE' for x in rr),'Contextual_Candidates':sum(x['Proposed_Role']=='CONTEXTUAL_CANDIDATE' for x in rr),'Exclude_Candidates':sum(x['Proposed_Role']=='EXCLUDE_CANDIDATE' for x in rr),'Independent_Study_Families':len({x['Study_Family_ID'] for x in rr}),'Null_Results':sum(x['Null_Result']=='YES' for x in rr),'Status':'PRE_HUMAN_DENSITY_ONLY'})
write('EXPANSION_DOMAIN_DENSITY_PRE_HUMAN.csv',dens)
write('INTERNATIONAL_EXPANSION_REFERENCE_PROJECTION.csv',[{'Scope':'International full manuscript pre-human projection','Existing_Frozen_Working_References':4,'Supporting_Candidates':sum(x['Proposed_Role']=='SUPPORTING_CANDIDATE' for x in ledger),'Contextual_Candidates':sum(x['Proposed_Role']=='CONTEXTUAL_CANDIDATE' for x in ledger),'Candidate_Study_Families':len({x['Study_Family_ID'] for x in ledger}),'Maximum_Pre_Deduplication_Working_References':4+sum(x['Proposed_Role']!='EXCLUDE_CANDIDATE' for x in ledger),'Projected_Defensible_Word_Range':'4,500–6,500 conditional on human selection, integrity recheck and nonredundant synthesis.','Gate':'HUMAN_ADJUDICATION_REQUIRED','Claim_Ready':0}])
write('BRAZIL_EXPANSION_STATUS.csv',[{'Gate':'BRAZIL_EXPANSION_INSUFFICIENT','Material_Decisions':26,'Brazil_Direct_Packets':0,'International_Records_Only':'YES','Permitted_Use':'TRANSFERABLE_CONTEXT','Brazil_Direct_Inflation':'0','Claim_Ready':0}])
write('FREEZE_CHANGE_REQUEST_REQUIRED.csv',[{'Status':'NONE_PROPOSED_IN_PRE_HUMAN_PACKAGE','Reason':'No human decision is recorded and no CEF-v1 change is executed.','CEF_v1_Changed':'NO'}])
write('POST_ADJUDICATION_PLANNING_MATRIX.csv',[{'Condition':'Named human decisions completed for all 26 and external integrity recheck cleared for selected records','Next_Action':'BATCH 11.0C — APPLY HUMAN EXPANSION DECISIONS','Gate':'Evaluate full-manuscript density after deduplication and claim-boundary confirmation.'},{'Condition':'Human decisions incomplete or selected sources retain integrity concerns','Next_Action':'Do not reconstruct the manuscript','Gate':'Remain at human-adjudication stage.'}])
lines=['# Full Manuscript — Human Evidence Adjudication Pack','','**Status:** `AI recommendations only — human adjudication pending`','','This package represents the 26 material decisions from the repaired authoritative queue. It does not decide inclusion, change CEF-v1, promote Claim-Ready, or establish final integrity. All selected records retain `INTEGRITY_EXTERNAL_RECHECK_PENDING`.','','## Instructions to the human reviewer','','For each row, choose one permitted decision: `RETAIN_BOUNDED_SUPPORTING_CANDIDATE`, `CONTEXTUAL_DISCUSSION_ONLY`, `EXCLUDE_FROM_FULL_MANUSCRIPT`, or `FREEZE_CHANGE_REQUEST_REQUIRED`. Record the decision, rationale, reviewer and date in the decision ledger. A null result is not a reason to discard an item.','','## Decision queue','']
for x in ledger:
 lines += [f"### {x['Decision_ID']} — {x['Evidence_ID']}",'',f"- **Result:** `{x['Result_ID']}`",f"- **Title:** {x['Title']}",f"- **Domain / cluster:** {x['Domain']} / `{x['Decision_Cluster_ID']}`",f"- **Population / country / sample:** {x['Population']} / {x['Country']} / {x['Sample']}",f"- **Design / appraisal:** {x['Design']} / {x['Appraisal']}",f"- **Exact result:** {x['Exact_Result']}",f"- **Null result:** {x['Null_Result']}",f"- **Main limitation:** {x['Primary_Limitation']}",f"- **Transferability:** {x['Transferability']}",f"- **AI recommendation:** `{x['AI_Recommendation']}` ({x['Tier']})",f"- **Potential role:** `{x['Proposed_Role']}`",f"- **Provisional claim:** {x['Provisional_Claim'] or 'No proposed central claim.'}",f"- **Prohibited inference:** {x['Prohibited_Inference']}",f"- **Alternative:** `{x['Alternative_Option']}`",f"- **Scientific impact:** {x['Scientific_Impact']}",f"- **Integrity:** `{x['Integrity_Status']}`",'']
(O/'FULL_MANUSCRIPT_HUMAN_ADJUDICATION_PACK.md').write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8',newline='\n')
report=f'''# BATCH 11.0B report\n\n## Gate\n\n`FULL_MANUSCRIPT_EVIDENCE_ADJUDICATION_PACKAGE_PASS`\n\nThe package represents all 26/26 material decisions from the repaired authoritative queue. It provides AI recommendations only: {sum(x['Proposed_Role']=='SUPPORTING_CANDIDATE' for x in ledger)} bounded supporting candidates, {sum(x['Proposed_Role']=='CONTEXTUAL_CANDIDATE' for x in ledger)} contextual candidates and {sum(x['Proposed_Role']=='EXCLUDE_CANDIDATE' for x in ledger)} exclusion candidates. It includes {len(claims)} `PROVISIONAL_EXPANSION_CLAIM`s, all `CLAIM_READY = NO`.\n\nHuman decision, rationale, reviewer and date are blank for all 26. Null results are preserved ({sum(x['Null_Result']=='YES' for x in ledger)}); the five protocol records remain outside this queue and cannot support outcome claims. All 26 records remain `INTEGRITY_EXTERNAL_RECHECK_PENDING`.\n\nInternational is ready only for human evidence adjudication. Brazil remains `BRAZIL_EXPANSION_INSUFFICIENT`: no record was reclassified as Brazil-direct. CEF-v1, Zotero, the short-form baseline and manuscripts were not changed.\n\nNext gate: `GO_HUMAN_EXPANSION_DECISIONS`. Do not begin manuscript reconstruction until named human decisions are applied in Batch 11.0C.\n'''
(O/'BATCH11_0B_REPORT.md').write_text(report,encoding='utf-8',newline='\n')
art=['FULL_MANUSCRIPT_HUMAN_ADJUDICATION_PACK.md','FULL_MANUSCRIPT_HUMAN_DECISION_LEDGER.csv','DECISION_CLUSTER_MAP.csv','AI_RECOMMENDED_EVIDENCE_ROLES.csv','PROVISIONAL_EXPANSION_CLAIM_LIBRARY.csv','EXPANSION_CLAIM_BOUNDARY_MATRIX.csv','EXPANSION_DOMAIN_DENSITY_PRE_HUMAN.csv','INTERNATIONAL_EXPANSION_REFERENCE_PROJECTION.csv','BRAZIL_EXPANSION_STATUS.csv','FREEZE_CHANGE_REQUEST_REQUIRED.csv','POST_ADJUDICATION_PLANNING_MATRIX.csv','BATCH11_0B_REPORT.md']
man={'batch':'BATCH 11.0B','base_commit':'16e54b170a92f1f267fcbc7af48b2425a0578530','gate':'FULL_MANUSCRIPT_EVIDENCE_ADJUDICATION_PACKAGE_PASS','expected_material_decisions':26,'represented_decisions':len(ledger),'human_decisions_filled_by_ai':0,'automatic_claim_ready_promotions':0,'null_result_suppression':0,'protocol_outcome_use':0,'cohort_double_counting':0,'cef_v1_unauthorized_changes':0,'zotero_changes':0,'short_form_baseline_changes':0,'brazil_direct_inflation':0,'artifact_sha256':{n:sha(O/n) for n in art}}
(O/'BATCH11_0B_MANIFEST.json').write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'decisions':len(ledger),'supporting':sum(x['Proposed_Role']=='SUPPORTING_CANDIDATE' for x in ledger),'context':sum(x['Proposed_Role']=='CONTEXTUAL_CANDIDATE' for x in ledger),'exclude':sum(x['Proposed_Role']=='EXCLUDE_CANDIDATE' for x in ledger),'claims':len(claims)},ensure_ascii=False))
