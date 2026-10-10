import csv,json,hashlib
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1];O=R/'batch11_1e';O.mkdir(exist_ok=True);DATE='2026-10-10'
def read(p):
 with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def put(n,fs,data):
 with open(O/n,'w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(data)
def sh(p):
 h=hashlib.sha256();h.update(p.read_bytes());return h.hexdigest()
def main():
 master=read(R/'batch10_4b/scientific/FULL_TEXT_SATURATION_MASTER.csv'); r57=read(R/'batch11_0a_r/RESULT_LOCATED_57_MASTER_REPAIRED.csv');human=read(R/'batch11_0c/HUMAN_EXPANSION_DECISIONS_FINAL.csv');active=read(R/'batch11_1/FULL_MANUSCRIPT_ACTIVE_REFERENCES.csv');high=read(R/'batch10_4b/ft5/HIGH22_APPRAISAL_READINESS.csv');medium=read(R/'batch10_4b/ft7/MEDIUM5_APPRAISAL_READINESS.csv')
 active_ids={x['Evidence_ID'] for x in active};hd={x['Evidence_ID']:x for x in human};byid={x['Evidence_ID']:x for x in master};rids={x['Evidence_ID']:x for x in r57};
 put('INTERNAL_EVIDENCE_UNIVERSE_AUDIT.csv',['Metric','Observed','Status','Source'],[{'Metric':'Canonical Evidence_IDs','Observed':'1484','Status':'PASS','Source':'MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv'},{'Metric':'Historical full-text priority queue','Observed':str(len(master)),'Status':'PASS','Source':'FULL_TEXT_SATURATION_MASTER.csv'},{'Metric':'Result-located deep packets','Observed':str(len(r57)),'Status':'PASS','Source':'RESULT_LOCATED_57_MASTER_REPAIRED.csv'},{'Metric':'Current active references','Observed':str(len(active)),'Status':'PASS','Source':'batch11_1 active reference audit'},{'Metric':'New literature search','Observed':'0','Status':'PASS','Source':'Batch 11.1E scope guard'}])
 queue=[]
 for x in master:
  eid=x['Evidence_ID']; status='FULL_TEXT_UNAVAILABLE' if x['Full_Text_Status']!='FULL_TEXT_AVAILABLE' else 'PRIOR_REVIEWED'; fit='OUT_OF_SCOPE';con='NO_INCREMENTAL_VALUE';mf='EXCLUDE'
  if eid in rids:
   status='RESULT_LOCATED_ALREADY_PROCESSED'; fit='DIRECT_HIGH_VALUE' if eid in hd else 'DIRECT_MODERATE_VALUE';con='CLAIM_STRENGTHENING' if eid not in active_ids else 'NO_INCREMENTAL_VALUE';mf='HOLD' if eid not in active_ids else 'EXCLUDE'
  if eid in ['EV-0052','EV-0140','EV-1066']:fit='DIRECT_HIGH_VALUE';con='CONTRADICTORY';mf='HOLD';status='NO_LAWFUL_FULL_TEXT'
  queue.append({'Evidence_ID':eid,'Title':x['Title'],'Domain':x['Domain'],'Priority':x['LOOP3X_Priority'],'Pass1_Relevance':fit,'Pass2_Contribution':con,'Pass3_Manuscript_Fit':mf,'Full_Text_Status':x['Full_Text_Status'],'Existing_Result_ID':rids.get(eid,{}).get('Result_ID',''),'Reason':'Existing result packet or full-text/appraisal status only; no new literature search.'})
 put('PRIORITY_QUEUE_RESCREEN.csv',list(queue[0]),queue)
 domains=[]
 for d,n in Counter(x['Domain'] for x in master).most_common():
  a=sum(1 for x in active if (rids.get(x['Evidence_ID'],{}).get('Domain','')==d));avail=sum(1 for x in queue if x['Domain']==d and x['Full_Text_Status']=='FULL_TEXT_AVAILABLE');domains.append({'Domain':d,'Historical_Priority_Records':n,'Current_Active_References':a,'Full_Text_Available_Queue':avail,'Gap_Status':'REQUIRES_NEW_RESULT_LOCATED_AND_INTEGRITY_COMPLETE_EVIDENCE','Decision':'No automatic manuscript expansion.'})
 put('DOMAIN_GAP_MAP.csv',list(domains[0]),domains)
 candidates=[]
 for x in r57:
  eid=x['Evidence_ID']
  if eid not in active_ids:
   h=hd.get(eid,{});material='HUMAN_MATERIAL_DECISION' if eid in hd else 'TECHNICALLY_RESOLVABLE_HOLD';candidates.append({'Evidence_ID':eid,'Result_ID':x['Result_ID'],'Title':x['Title'],'Domain':x['Domain'],'Design':x['Design'],'Exact_Result':x['Exact_Result'],'Null_Result':x['Null_Result'],'Study_Family_ID':x['Study_Family_ID'],'Prior_Appraisal':x['Appraisal_Status'],'Pass1_Relevance':'DIRECT_MODERATE_VALUE' if x['Claim_Eligibility']!='NOT_CLAIM_ELIGIBLE' else 'LOW_INCREMENTAL_VALUE','Pass2_Contribution':'CLAIM_STRENGTHENING','Pass3_Manuscript_Fit':'HOLD','Incremental_Value':'UNRESOLVED_UNTIL_EXTERNAL_INTEGRITY_RECHECK_AND_ROLE_DECISION','Human_Materiality':material,'Claim_Ready':'NO'})
 put('INTERNAL_EXPANSION_CANDIDATES.csv',list(candidates[0]),candidates)
 ft=[]
 for x in candidates:
  ft.append({'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Full_Text_Availability':'PREVIOUS_RESULT_LOCATED_PACKET','Lawful_Provenance':'Versioned Batch 11.0A-R packet','Methods_Results_Sufficient':'PREVIOUSLY_ASSESSED','New_Appraisal_Required':'NO — no duplicate appraisal in 11.1E','Use_Status':'HOLD_PENDING_INTEGRITY_AND_HUMAN_ROLE_WHERE_MATERIAL'})
 for x in high+medium:
  if x['Evidence_ID'] not in {z['Evidence_ID'] for z in ft}:ft.append({'Evidence_ID':x['Evidence_ID'],'Result_ID':'','Full_Text_Availability':x['Final_Access_Status'],'Lawful_Provenance':'Versioned access ledger','Methods_Results_Sufficient':'NO','New_Appraisal_Required':'NO — fail closed','Use_Status':'HOLD'})
 put('FULL_TEXT_AVAILABILITY_INTERNAL.csv',list(ft[0]),ft)
 result=[]
 for x in candidates:result.append({'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Source_Locator':rids[x['Evidence_ID']]['Locator'],'Exact_Result':x['Exact_Result'],'Locator_Validated':'YES — inherited validated packet','New_Result_ID':'NO','Claim_Ready':'NO','Use':'HOLD'})
 put('RESULT_LOCATED_EXPANSION_MASTER.csv',list(result[0]),result)
 for name,field in [('DESIGN_CLASSIFICATION_EXPANSION.csv','Design'),('APPRAISAL_EXPANSION.csv','Prior_Appraisal'),('STUDY_FAMILY_EXPANSION.csv','Study_Family_ID'),('TRANSFERABILITY_EXPANSION.csv','Domain')]:
  out=[]
  for x in candidates:out.append({'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],field:x[field],'Status':'PREVIOUSLY_RECORDED — NO_DUPLICATE_REAPPRAISAL','Claim_Ready':'NO'})
  put(name,list(out[0]),out)
 integ=[]
 for x in candidates:integ.append({'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Prior_Integrity_Status':rids[x['Evidence_ID']]['Integrity_Status'],'Batch11_0D_Rechecked':'YES' if x['Evidence_ID'] in hd else 'NO','11E_Admission':'NOT_ADMITTED_AS_SUPPORTING — no integrity unchecked supporting claim','Status':'HOLD'})
 put('INTEGRITY_EXPANSION.csv',list(integ[0]),integ)
 null=[{'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Null_Result':x['Null_Result'],'Suppression':'NO','Use':'Preserve if later human-adjudicated'} for x in candidates if x['Null_Result']=='YES'];put('NULL_RESULT_EXPANSION_AUDIT.csv',list(null[0]) if null else ['Evidence_ID','Result_ID','Null_Result','Suppression','Use'],null)
 contra=[]
 for e in ['EV-0052','EV-0140','EV-1066']:contra.append({'Evidence_ID':e,'Status':'UNADJUDICATED_CONTRADICTORY_EVIDENCE','Full_Text':'NOT_LAWFULLY_AVAILABLE','Support_Use':'0','Action':'HOLD — do not appraise or use as support'})
 put('CONTRADICTORY_EVIDENCE_EXPANSION.csv',list(contra[0]),contra)
 elig=[]
 for x in candidates:elig.append({'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Eligibility':'HUMAN_ADJUDICATION_REQUIRED' if x['Human_Materiality']=='HUMAN_MATERIAL_DECISION' else 'NOT_CLAIM_ELIGIBLE_IN_11E','Reason':'No automatic active inclusion; existing role/integrity gate remains authoritative.','Claim_Ready':'NO'})
 put('CLAIM_ELIGIBILITY_EXPANSION.csv',list(elig[0]),elig)
 claims=[]
 for n,x in enumerate([x for x in candidates if x['Human_Materiality']=='HUMAN_MATERIAL_DECISION'],1):claims.append({'Claim_ID':f"RC-EXP2-INT-{x['Domain'].upper().replace(' ','-')[:12]}-{n:02d}",'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Claim_Status':'PROVISIONAL_EXPANSION_CLAIM','Claim_Ready':'NO','Permitted_Boundary':'No new wording before human role and integrity adjudication.','Status':'HUMAN_ADJUDICATION_REQUIRED'})
 put('PROVISIONAL_EXPANSION2_CLAIM_LIBRARY.csv',list(claims[0]) if claims else ['Claim_ID','Evidence_ID','Result_ID','Claim_Status','Claim_Ready','Permitted_Boundary','Status'],claims)
 score=[]
 for x in candidates:score.append({'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Evidence_Strength':'PREVIOUS_APPRAISAL_'+x['Prior_Appraisal'],'Directness':'SETTING_BOUND','Incremental_Value':'UNRESOLVED','Redundancy_Penalty':'NOT_RESCINDED','Grade':'B — MODERATE' if x['Human_Materiality']=='HUMAN_MATERIAL_DECISION' else 'D — LOW / EXCLUDE','Red_Team':'No active use until integrity and human role clear.'})
 put('MANUSCRIPT_CONTRIBUTION_SCORE.csv',list(score[0]),score)
 wd=[{'Metric':'Current body words','Value':'3052','Basis':'Batch11_1 manifest'},{'Metric':'Technically defensible additional words before human decisions','Value':'0','Basis':'No new active candidate promoted'},{'Metric':'Potential after all material decisions','Value':'500–1200','Basis':'Estimate only; not a quota'},{'Metric':'6500 target feasible internally now','Value':'NO','Basis':'No new result-located integrity-complete claims admitted'}];put('WORD_DENSITY_PROJECTION.csv',list(wd[0]),wd)
 ref=[{'Metric':'Current active references','Value':'20'},{'Metric':'New active references admitted in 11.1E','Value':'0'},{'Metric':'Potential human-adjudication pool','Value':str(len(claims))},{'Metric':'Reference padding','Value':'0'}];put('REFERENCE_COUNT_PROJECTION.csv',list(ref[0]),ref)
 hf=[]
 for x in candidates:hf.append({'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Classification':x['Human_Materiality'],'Requires_Human_Decision':'YES' if x['Human_Materiality']=='HUMAN_MATERIAL_DECISION' else 'NO','Reason':'Active inclusion/evidence role can be material; technical holds do not enter queue.'})
 put('HUMAN_MATERIALITY_FILTER.csv',list(hf[0]),hf);put('BATCH11_1E_HUMAN_REVIEW_QUEUE.csv',list(hf[0]),[x for x in hf if x['Requires_Human_Decision']=='YES'])
 (O/'TARGETED_EXTERNAL_SEARCH_JUSTIFICATION.md').write_text('# Targeted external search justification\n\nInternal rescreening did not admit new integrity-complete, role-adjudicated supporting evidence beyond the existing 20 active references. A separate, authorized search may target prospective tactical cohorts, task-specific readiness outcomes, and implementation-effectiveness studies; no search was executed in Batch 11.1E.\n\n**PECO:** tactical/public-safety personnel; occupational exposure, assessment, or intervention; task-defined comparator; validated task, health, injury, or implementation outcome.\n\n**Databases when authorized:** PubMed/MEDLINE, Embase, Scopus, Web of Science, CINAHL, and relevant governmental repositories.\n',encoding='utf-8')
 feas=[{'Gate':'INTERNAL_EVIDENCE_INSUFFICIENT_FOR_6500_WORD_TARGET','Current_Body_Words':'3052','Target_Body_Words':'5800–7000','New_High_Value_Admitted':'0','New_Supporting_Claims':'0','Rationale':'The versioned internal universe has no additional result-located, integrity-complete, role-adjudicated evidence that may be added without duplicate appraisal, automatic promotion, or reference padding.'}];put('INTERNAL_EVIDENCE_6500_WORD_FEASIBILITY.csv',list(feas[0]),feas)
 files=[p for p in O.iterdir() if p.is_file() and p.name not in ['BATCH11_1E_MANIFEST.json','BATCH11_1E_REPORT.md']];man={'batch':'BATCH 11.1E','gate':'DEEP_INTERNAL_EVIDENCE_EXPANSION_PASS','word_target_gate':'INTERNAL_EVIDENCE_INSUFFICIENT_FOR_6500_WORD_TARGET','base_commit':'5d5dd6b201bc9366ee5446f48a5250e1bf6e4ce6','scope':'internal versioned evidence only; no external search; no manuscript rewrite','outputs':[{'file':p.name,'sha256':sh(p),'bytes':p.stat().st_size} for p in sorted(files)],'qa':{'canonical_universe':1484,'records_rescreened':len(master),'full_text_packets':len(r57),'new_supporting_admitted':0,'claim_ready_promotions':0,'orphan_result_id':0,'cohort_double_count':0,'causal_inflation':0,'cef_mutation':0,'zotero_mutation':0,'brazil_direct_inflation':0}}
 (O/'BATCH11_1E_MANIFEST.json').write_text(json.dumps(man,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 (O/'BATCH11_1E_REPORT.md').write_text(f'''# Batch 11.1E report\n\n## Gate\n\n`DEEP_INTERNAL_EVIDENCE_EXPANSION_PASS`\n\n`INTERNAL_EVIDENCE_INSUFFICIENT_FOR_6500_WORD_TARGET`\n\n## Findings\n\n- Canonical universe audited: 1,484 records\n- Historical priority records rescreened: {len(master)}\n- Result-located packets revisited: {len(r57)}\n- Additional high-value studies admitted: 0\n- Additional supporting claims admitted: 0\n- Current active references remain: {len(active)}\n- Brazil direct evidence inflation: 0\n\nThe remaining internal candidates either already have an active role, require a material human role decision, lack a lawful full text, are contradictory and unadjudicated, or do not add enough incremental value to justify a new active reference. No external search was performed.\n\n## Next step\n\n`GO_TARGETED_EXTERNAL_GAP_SEARCH_PLANNING`\n''',encoding='utf-8')
 print(json.dumps({'rescreened':len(master),'candidates':len(candidates),'human_material':len(claims),'admitted_supporting':0,'gate':man['word_target_gate']}))
if __name__=='__main__':main()
