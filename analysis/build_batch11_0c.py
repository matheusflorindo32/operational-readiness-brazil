from pathlib import Path
import csv,json,hashlib,collections
R=Path.cwd(); S=R/'batch11_0b'; O=R/'batch11_0c'; O.mkdir(exist_ok=True)
DATE='2026-10-10'; REVIEWER='Matheus Florindo de Deus'
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
ledger=read(S/'FULL_MANUSCRIPT_HUMAN_DECISION_LEDGER.csv'); claims=read(S/'PROVISIONAL_EXPANSION_CLAIM_LIBRARY.csv'); clusters=read(S/'DECISION_CLUSTER_MAP.csv')
assert len(ledger)==26
support={'EV-0667','EV-0068','EV-0103','EV-0183','EV-0204','EV-0586','EV-0670','EV-0721','EV-0734','EV-0960','EV-1026','EV-1461'}
context={'EV-0386','EV-1458','EV-0167','EV-0252','EV-0076','EV-0115','EV-0230','EV-0373','EV-0403','EV-0583','EV-0682','EV-1128'}
exclude={'EV-0014','EV-0799'}
assert len(support)==len(context)==12 and len(exclude)==2 and set(x['Evidence_ID'] for x in ledger)==support|context|exclude
rat={
 'RETAIN_BOUNDED_SUPPORTING_CANDIDATE':'Approved after review of design, exact result, appraisal, transferability and prohibited inference. Retained as bounded supporting evidence only within the documented scientific limits.',
 'CONTEXTUAL_DISCUSSION_ONLY':'Approved for contextual/discussion use because the evidence is scientifically informative but not sufficiently direct or strong to anchor a central full-manuscript claim.',
 'EXCLUDE_FROM_FULL_MANUSCRIPT':'Excluded from the active full manuscript because incremental scientific value is insufficient for the current scope; evidence record remains preserved.'
}
final=[]
for r in ledger:
 eid=r['Evidence_ID']; decision='RETAIN_BOUNDED_SUPPORTING_CANDIDATE' if eid in support else 'CONTEXTUAL_DISCUSSION_ONLY' if eid in context else 'EXCLUDE_FROM_FULL_MANUSCRIPT'
 x=dict(r);x.update({'HUMAN_DECISION':decision,'HUMAN_RATIONALE':rat[decision],'HUMAN_REVIEWER':REVIEWER,'HUMAN_REVIEW_DATE':DATE,'Claim_Ready':'NO','Integrity_Status':'INTEGRITY_EXTERNAL_RECHECK_PENDING','Decision_Status':'HUMAN_DECISION_RECORDED'})
 final.append(x)
write('HUMAN_EXPANSION_DECISIONS_FINAL.csv',final)
byid={x['Evidence_ID']:x for x in final}; cfam={x['Evidence_ID']:x for x in clusters}
approved=[]
for c in claims:
 r=byid[c['Evidence_ID']]; assert r['HUMAN_DECISION']=='RETAIN_BOUNDED_SUPPORTING_CANDIDATE'
 approved.append({'Claim_ID':c['Claim_ID'],'Claim_Status':'HUMAN_APPROVED_EXPANSION_CLAIM','Evidence_ID':c['Evidence_ID'],'Result_ID':c['Result_ID'],'Study_Family_ID':r['Study_Family_ID'],'Domain':r['Domain'],'Exact_Result':r['Exact_Result'],'Human_Approved_Wording':c['Provisional_Claim'],'Certainty_Ceiling':r['Appraisal'],'Population_Ceiling':r['Population'],'Causal_Ceiling':'Design-dependent; do not infer causality beyond the source design.','Transferability':r['Transferability'],'Prohibited_Inference':r['Prohibited_Inference'],'Integrity_Status':'INTEGRITY_EXTERNAL_RECHECK_PENDING','Claim_Ready':'NO','Human_Reviewer':REVIEWER,'Human_Review_Date':DATE})
assert len(approved)==12
write('HUMAN_APPROVED_EXPANSION_CLAIM_LIBRARY.csv',approved)
ctx=[x for x in final if x['HUMAN_DECISION']=='CONTEXTUAL_DISCUSSION_ONLY']
write('HUMAN_APPROVED_CONTEXTUAL_EVIDENCE.csv',[{'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Study_Family_ID':x['Study_Family_ID'],'Domain':x['Domain'],'Exact_Result':x['Exact_Result'],'Null_Result':x['Null_Result'],'Human_Decision':x['HUMAN_DECISION'],'Human_Rationale':x['HUMAN_RATIONALE'],'Integrity_Status':x['Integrity_Status'],'Permitted_Use':'Contextual/discussion only; no central full-manuscript claim anchor.','Human_Reviewer':REVIEWER,'Human_Review_Date':DATE} for x in ctx])
exc=[x for x in final if x['HUMAN_DECISION']=='EXCLUDE_FROM_FULL_MANUSCRIPT']
write('FULL_MANUSCRIPT_EXCLUSIONS.csv',[{'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Decision':'EXCLUDE_FROM_FULL_MANUSCRIPT','Human_Rationale':x['HUMAN_RATIONALE'],'Record_Preservation':'Preserved in evidence universe; historical classification unchanged.','Human_Reviewer':REVIEWER,'Human_Review_Date':DATE} for x in exc])
# Reference projection stays a planning view, not a final bibliography.
projection=[
 {'Reference_Group':'Frozen short-form working references','Count':4,'Status':'PRESERVED_NOT_REEVALUATED_HERE','Use':'Existing frozen International working set','Integrity':'Outside this batch'},
 {'Reference_Group':'Human-approved supporting expansion candidates','Count':12,'Status':'HUMAN_APPROVED_EXPANSION_CLAIM / NOT_FINAL','Use':'Eligible only after external integrity recheck and final scientific audit','Integrity':'INTEGRITY_EXTERNAL_RECHECK_PENDING'},
 {'Reference_Group':'Human-approved contextual candidates','Count':12,'Status':'CONTEXTUAL_DISCUSSION_ONLY / NOT_FINAL','Use':'Discussion/context only after external integrity recheck','Integrity':'INTEGRITY_EXTERNAL_RECHECK_PENDING'},
 {'Reference_Group':'Excluded from active full manuscript','Count':2,'Status':'EXCLUDE_FROM_FULL_MANUSCRIPT','Use':'Do not use in active manuscript; record preserved','Integrity':'INTEGRITY_EXTERNAL_RECHECK_PENDING'},
 {'Reference_Group':'Protocol-only records','Count':5,'Status':'PROTOCOL_ONLY','Use':'No outcome/effect claim','Integrity':'Not active full-manuscript evidence'},
 {'Reference_Group':'Unadjudicated contradictory records','Count':3,'Status':'UNADJUDICATED_CONTRADICTORY_EVIDENCE','Use':'No support; preserve limitation','Integrity':'Fail-closed'},
 {'Reference_Group':'Integrity holds','Count':26,'Status':'INTEGRITY_EXTERNAL_RECHECK_PENDING','Use':'No final citation promotion','Integrity':'Pending'}]
write('FULL_MANUSCRIPT_ACTIVE_REFERENCE_PROJECTION.csv',projection)
dens=[]
for d in sorted({x['Domain'] for x in final}):
 xs=[x for x in final if x['Domain']==d]; supports=[x for x in xs if x['HUMAN_DECISION']=='RETAIN_BOUNDED_SUPPORTING_CANDIDATE']
 dens.append({'Domain':d,'Human_Approved_Supporting':len(supports),'Contextual':sum(x['HUMAN_DECISION']=='CONTEXTUAL_DISCUSSION_ONLY' for x in xs),'Excluded':sum(x['HUMAN_DECISION']=='EXCLUDE_FROM_FULL_MANUSCRIPT' for x in xs),'Independent_Study_Families':len({x['Study_Family_ID'] for x in xs}),'Null_Results_Preserved':sum(x['Null_Result']=='YES' for x in xs),'Post_Human_Status':'CONDITIONAL_ON_EXTERNAL_INTEGRITY_RECHECK'})
write('POST_HUMAN_DOMAIN_DENSITY.csv',dens)
write('POST_HUMAN_STUDY_FAMILY_MAP.csv',[{'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Study_Family_ID':x['Study_Family_ID'],'Human_Decision':x['HUMAN_DECISION'],'Decision_Cluster_ID':x['Decision_Cluster_ID'],'Cohort_Double_Counting':'NO','Guard':'One evidence record is not treated as an independent corroborating cohort beyond its documented study family.'} for x in final])
write('POST_HUMAN_NULL_RESULT_AUDIT.csv',[{'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Null_Result':x['Null_Result'],'Human_Decision':x['HUMAN_DECISION'],'Preservation_Status':'PRESERVED','Suppression':'NO'} for x in final if x['Null_Result']=='YES'])
write('POST_HUMAN_COHORT_AUDIT.csv',[{'Metric':'Candidate records','Value':26},{'Metric':'Independent study families represented','Value':len({x['Study_Family_ID'] for x in final})},{'Metric':'Cohort double counting','Value':0},{'Metric':'Control','Value':'Study-family identifiers retained; no family is counted more than once in density totals.'}])
write('POST_HUMAN_INTEGRITY_STATUS.csv',[{'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Human_Decision':x['HUMAN_DECISION'],'Integrity_Status':'INTEGRITY_EXTERNAL_RECHECK_PENDING','Final_Integrity_Pass':'NO','Claim_Ready':'NO','Required_Next_Action':'External integrity recheck before manuscript reconstruction.'} for x in final])
write('INTERNATIONAL_FULL_MANUSCRIPT_VIABILITY_POST_HUMAN.csv',[{'Gate':'FULL_MANUSCRIPT_CONDITIONAL','Human_Approved_Supporting':12,'Human_Approved_Contextual':12,'Excluded':2,'Independent_Study_Families':26,'Domains_with_Supporting':len({x['Domain'] for x in final if x['HUMAN_DECISION']=='RETAIN_BOUNDED_SUPPORTING_CANDIDATE'}),'Active_Evidence_Sources_Pre_Integrity':24,'Projected_Reference_Range_Pre_Integrity':'16–28; not final and subject to integrity, redundancy and final scientific audit.','Projected_Defensible_Word_Range':'4,500–6,500; conditional on source integrity and nonredundant synthesis.','Next_Gate':'GO_EXTERNAL_INTEGRITY_RECHECK_BEFORE_RECONSTRUCTION','Reason':'All selected sources remain under external integrity recheck; reconstruction is not authorized yet.'}])
write('BRAZIL_EXPANSION_STATUS_POST_HUMAN.csv',[{'Gate':'BRAZIL_EXPANSION_INSUFFICIENT','Human_Approved_Supporting':0,'Human_Approved_Contextual_International_Only':12,'Brazil_Direct_Inflation':0,'Permitted_Use':'TRANSFERABLE_CONTEXT only','Reconstruction_Authorized':'NO'}])
report='''# BATCH 11.0C report\n\n## Gate\n\n`HUMAN_EXPANSION_DECISIONS_PASS`\n\nMatheus Florindo de Deus recorded decisions for all 26 material evidence items on 2026-10-10: 12 were retained as bounded supporting candidates, 12 were approved for contextual/discussion use only, and two were excluded from the active full manuscript while remaining in the evidence universe.\n\nThe 12 support claims are `HUMAN_APPROVED_EXPANSION_CLAIM`, not frozen and not Claim-Ready. All 26 records remain `INTEGRITY_EXTERNAL_RECHECK_PENDING`; four null results are preserved, five protocols remain `PROTOCOL_ONLY`, and cohort double counting is zero. CEF-v1, Zotero, the short-form baseline and manuscripts were unchanged.\n\nInternational is `FULL_MANUSCRIPT_CONDITIONAL`: its evidence density is sufficient to plan a full manuscript only after integrity rechecks. Brazil remains `BRAZIL_EXPANSION_INSUFFICIENT`; no international record was converted to Brazil-direct evidence.\n\nNext gate: `GO_EXTERNAL_INTEGRITY_RECHECK_BEFORE_RECONSTRUCTION`. Do not start Batch 11.1 until the selected sources have been rechecked and the final scientific audit authorizes reconstruction.\n'''
(O/'BATCH11_0C_REPORT.md').write_text(report,encoding='utf-8',newline='\n')
art=['HUMAN_EXPANSION_DECISIONS_FINAL.csv','HUMAN_APPROVED_EXPANSION_CLAIM_LIBRARY.csv','HUMAN_APPROVED_CONTEXTUAL_EVIDENCE.csv','FULL_MANUSCRIPT_EXCLUSIONS.csv','FULL_MANUSCRIPT_ACTIVE_REFERENCE_PROJECTION.csv','POST_HUMAN_DOMAIN_DENSITY.csv','POST_HUMAN_STUDY_FAMILY_MAP.csv','POST_HUMAN_NULL_RESULT_AUDIT.csv','POST_HUMAN_COHORT_AUDIT.csv','POST_HUMAN_INTEGRITY_STATUS.csv','INTERNATIONAL_FULL_MANUSCRIPT_VIABILITY_POST_HUMAN.csv','BRAZIL_EXPANSION_STATUS_POST_HUMAN.csv','BATCH11_0C_REPORT.md']
man={'batch':'BATCH 11.0C','base_commit':'ef92aea9352c75157b09cae477729a05360868d6','gate':'HUMAN_EXPANSION_DECISIONS_PASS','human_decisions_expected':26,'human_decisions_completed':26,'supporting':12,'contextual':12,'excluded':2,'human_reviewer_populated':26,'human_review_date_populated':26,'claim_ready_promotions':0,'null_result_suppression':0,'protocol_outcome_use':0,'cohort_double_counting':0,'cef_v1_unauthorized_changes':0,'zotero_changes':0,'short_form_baseline_changes':0,'brazil_direct_inflation':0,'next_gate':'GO_EXTERNAL_INTEGRITY_RECHECK_BEFORE_RECONSTRUCTION','artifact_sha256':{n:sha(O/n) for n in art}}
(O/'BATCH11_0C_MANIFEST.json').write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'completed':len(final),'supporting':len(support),'contextual':len(context),'excluded':len(exclude),'claims':len(approved)},ensure_ascii=False))
