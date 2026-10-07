"""Consolidate retained-reference packets without inventing unextracted results."""
import csv,json
from collections import Counter,defaultdict
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'batch10_4f_r1b1b'
def rd(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def wr(p,f,rows):
 p.parent.mkdir(exist_ok=True)
 with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=f,extrasaction='ignore');w.writeheader();w.writerows(rows)
def main():
 inv=rd(R/'batch10_4f_r1b1'/'FINAL_16_REFERENCE_SOURCE_INVENTORY.csv'); rec={x['Evidence_ID']:x for x in rd(R/'batch10_4f_r1b1a'/'TARGETED_SOURCE_RECOVERY_LEDGER.csv')}
 p1=rd(R/'batch10_4f_r1b1'/'RESULT_LEVEL_EVIDENCE_LEDGER.csv'); p2=rd(R/'batch10_4f_r1b1a'/'NEW_RESULT_LEVEL_EVIDENCE_LEDGER.csv'); results=[]
 for x in p1:results.append(dict(x,Source_Depth='FULL_TEXT_VERIFIED'))
 for x in p2:results.append({'Evidence_ID':x['Evidence_ID'],'Result_ID':x['Result_ID'],'Source_Section':x['Source_Section'],'Source_Subsection':'NR','Page_Number':'NR_ABSTRACT','Paragraph_or_Locator':x['Source_Locator'],'Table_Number':'NR','Figure_Number':'NR','Outcome':'Abstract result available; bounded extraction pending human paraphrase','Exposure_or_Intervention':'NR','Comparator':'NR','Population':x['Population'],'Sample_Size':'NR','Effect_Estimate':x['Effect_Estimate'],'CI':'NR','P_value':'NR','Direction':'NR','Null_Result':'NR','Author_Interpretation':'NR','Methodological_Limitation':'Abstract-only depth','Transferability_Limitation':'No unreported design details inferred.','Source_Depth':'ABSTRACT_RESULT_ONLY'})
 byev=defaultdict(list)
 for x in results:byev[x['Evidence_ID']].append(x)
 packets=[];depth=[];scope=[];prohibit=[];transfer=[];nulls=[];cohort=[];insufficient=[]
 for x in inv:
  ev=x['Evidence_ID']; status=rec.get(ev,{}).get('Final_Access_Status',x['Full_Text_Status'])
  if ev in {'EV-1473','EV-1484'}:d='FULL_TEXT_VERIFIED';src='VERIFIED_OFFICIAL_FULL_TEXT'
  elif status=='VERIFIED_OPEN_FULL_TEXT':d='FULL_TEXT_VERIFIED';src=status
  elif status=='VERIFIED_GOVERNMENT_SOURCE':d='GOVERNMENT_FULL_SOURCE_VERIFIED';src=status
  elif status=='ABSTRACT_ONLY_CONFIRMED':d='ABSTRACT_RESULT_ONLY';src=status
  else:d='SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT';src=status
  rids=';'.join(y['Result_ID'] for y in byev[ev]) or 'NONE'
  packet={'Reference_Number':x['Reference_Number'],'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Exact_Title':x['Exact_Title'],'Authors':x['Authors'],'Year':x['Year'],'Journal_or_Source':x['Journal'],'DOI':x['DOI'],'PMID':x['PMID'],'PMCID':x['PMCID'],'Current_Evidence_Role':x['Current_Evidence_Role'],'Source_Depth':d,'Source_Type':src,'Source_URL_or_Path':rec.get(ev,{}).get('Recovery_URL','Prior verified PMC/PubMed source'),'Access_Date':rec.get(ev,{}).get('Recovery_Date','2026-10-07'),'File_Hash':'See upstream provenance/manifest','Identity_Status':'REJECTED_LEGACY_IDENTITY' if ev=='EV-1474' else ('PASS' if d in {'FULL_TEXT_VERIFIED','GOVERNMENT_FULL_SOURCE_VERIFIED'} else 'NOT_VERIFIED_FOR_FULL_TEXT'),'Version_Status':'RETAINED_V013_NO_FREEZE','Study_Design':'NR — see canonical master','Setting':'NR','Population':'NR — see canonical master','Sample_Size':'NR','Country':'NR','Tactical_Population_Type':'NR','Exposure':'NR','Intervention':'NR','Comparator':'NR','Duration':'NR','Primary_Outcome':'NR','Secondary_Outcomes':'NR','Result_IDs':rids,'Packet_Completion':'RESULT_LOCALIZED' if rids!='NONE' else 'RESULT_LEVEL_SUPPORT_UNAVAILABLE'}
  packets.append(packet);depth.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Source_Depth':d,'Reason':src,'Result_Level_Status':packet['Packet_Completion']})
  permitted='Only a source-located result bounded by its documented population, outcome, and design.' if rids!='NONE' else 'No result-level claim permitted until a source locator is extracted.'
  forbidden='No causal, universal-readiness, national-prevalence, or cross-population inference.'
  scope.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'PERMITTED_CLAIM_SCOPE':permitted});prohibit.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'PROHIBITED_INFERENCE':forbidden})
  transfer.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Classification':'DIRECT_BRAZIL_PUBLIC_SAFETY' if ev.startswith('EV-14') else 'TACTICAL_INDIRECT','Justification':'Requires source-level population confirmation before claim use.'})
  cohort.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Cohort_Relation':'CF-BR-PMES-CFO-2023-01; independent cohort count=1' if ev in {'EV-1473','EV-1474'} else 'NO_KNOWN_SHARED_COHORT_IN_CURRENT_PACKET','Rule':'Do not treat cohort-family records as independent replications.'})
  if d=='SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT' or (d in {'FULL_TEXT_VERIFIED','GOVERNMENT_FULL_SOURCE_VERIFIED'} and rids=='NONE'):
   insufficient.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Source_Depth':d,'Current_Use':f"International {x['International_Use']}; Brazil {x['Brazil_Use']}",'Status':'RETAINABILITY_PENDING_SENTENCE_READJUDICATION','Likely_Requirement':'RESULT_LEVEL_SUPPORT_UNAVAILABLE; narrowing/deletion may be required.'})
 for r in results:
  if r['Null_Result'] in {'YES','HISTORICAL_NULL_RETAINED'}:nulls.append({'Evidence_ID':r['Evidence_ID'],'Result_ID':r['Result_ID'],'Null_Result':r['Null_Result'],'Preservation':'YES'})
 for ev,note in [('EV-1474','Historical null-result status retained but not re-localized; identity remains unresolved.'),('EV-1479','Historical null-result status retained; recovered full source still awaits result extraction.')]:nulls.append({'Evidence_ID':ev,'Result_ID':'NOT_RELOCALIZED','Null_Result':'HISTORICAL_NULL_RETAINED','Preservation':note})
 adj=rd(R/'batch10_4f_r1b'/'SENTENCE_SUPPORT_ADJUDICATION.csv'); cross=[]
 for s in adj:
  evs=[z for z in s['Evidence_ID'].split(';') if z]; cand=[z['Result_ID'] for e in evs for z in byev[e]]
  status='POTENTIAL_PARTIAL' if cand else ('SOURCE_INSUFFICIENT' if any(next((d['Source_Depth'] for d in depth if d['Evidence_ID']==e),'').startswith('SOURCE_INSUFFICIENT') for e in evs) else 'NO_RESULT_SUPPORT')
  cross.append({'Sentence_ID':s['Sentence_ID'],'Existing_Reference_Number':s['Reference_Number'],'Existing_Reference_ID':s['Reference_ID'],'Evidence_ID':s['Evidence_ID'],'Candidate_Result_ID':';'.join(cand),'Source_Depth':';'.join(next(d['Source_Depth'] for d in depth if d['Evidence_ID']==e) for e in evs),'Candidate_Support_Fit':status})
 changes=[x for x in adj if x['Final_Disposition']=='CITATION_CHANGE_REQUIRED'];nar=[x for x in adj if x['Final_Disposition']=='NARROWING_REQUIRED']
 def cov(rows):
  return [next(x for x in cross if x['Sentence_ID']==r['Sentence_ID']) | {'Coverage':'RESULT_AVAILABLE_FOR_CURRENT_REFERENCE' if next(x for x in cross if x['Sentence_ID']==r['Sentence_ID'])['Candidate_Result_ID'] else 'NO_RESULT_LEVEL_SUPPORT'} for r in rows]
 fields=list(packets[0]);wr(O/'CONSOLIDATED_16_REFERENCE_EVIDENCE_PACKETS.csv',fields,packets);rf=list(results[0]) if results else ['Evidence_ID'];wr(O/'CONSOLIDATED_RESULT_LEVEL_EVIDENCE_LEDGER.csv',rf,results);wr(O/'CONSOLIDATED_RESULT_SOURCE_LOCATORS.csv',['Evidence_ID','Result_ID','Source_Section','Paragraph_or_Locator','Page_Number','Source_Depth'],[{k:x[k] for k in ['Evidence_ID','Result_ID','Source_Section','Paragraph_or_Locator','Page_Number','Source_Depth']} for x in results]);wr(O/'REFERENCE_SOURCE_DEPTH_FINAL.csv',list(depth[0]),depth);wr(O/'REFERENCE_PERMITTED_CLAIM_SCOPE_FINAL.csv',list(scope[0]),scope);wr(O/'REFERENCE_PROHIBITED_INFERENCE_FINAL.csv',list(prohibit[0]),prohibit);wr(O/'REFERENCE_TRANSFERABILITY_FINAL.csv',list(transfer[0]),transfer);wr(O/'REFERENCE_NULL_RESULT_FINAL.csv',list(nulls[0]),nulls);wr(O/'REFERENCE_COHORT_RELATION_FINAL.csv',list(cohort[0]),cohort);wr(O/'INSUFFICIENT_SOURCE_REFERENCE_STATUS.csv',list(insufficient[0]),insufficient);wr(O/'SENTENCE_RESULT_CANDIDATE_CROSSWALK_V2.csv',list(cross[0]),cross);wr(O/'CITATION_CHANGE_COVERAGE_V2.csv',list(cov(changes)[0]),cov(changes));wr(O/'NARROWING_COVERAGE_V2.csv',list(cov(nar)[0]),cov(nar));wr(O/'EV1474_IDENTITY_STATUS_FINAL.csv',['Evidence_ID','Status','Rule','Action'],[{'Evidence_ID':'EV-1474','Status':'PMC3382270_REJECTED_LEGACY_IDENTITY; FULL_TEXT_ROUTE_IDENTITY_UNRESOLVED','Rule':'No result-level support use','Action':'FREEZE_CHANGE_REQUEST_CANDIDATE only if a frozen PMCID correction is proposed.'}])
 c=Counter(x['Source_Depth'] for x in depth);man={'gate':'EVIDENCE_PACKET_CONSOLIDATION_BLOCKED','references_packetized':len(packets),'full_text_verified':c['FULL_TEXT_VERIFIED'],'government_verified':c['GOVERNMENT_FULL_SOURCE_VERIFIED'],'abstract_result_only':c['ABSTRACT_RESULT_ONLY'],'insufficient':c['SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT'],'result_ids':len(results),'auditable_locators':len(results),'candidate_crosswalk_coverage':sum(bool(x['Candidate_Result_ID']) for x in cross),'source_insufficient_sentence_uses':sum(x['Candidate_Support_Fit']=='SOURCE_INSUFFICIENT' for x in cross),'forced_semantic_links':0,'reason':'Packets distinguish every source depth, but five newly recovered full texts lack result-level extraction and seven references remain source-insufficient; sentence readjudication would still force support.'}
 (O/'BATCH10_4F_R1B1B_MANIFEST.json').write_text(json.dumps(man,indent=2)+'\n');(O/'BATCH10_4F_R1B1B_REPORT.md').write_text(f"# Consolidated evidence packets\n\n`EVIDENCE_PACKET_CONSOLIDATION_BLOCKED`\n\nAll {len(packets)}/16 references have one packet. The source-depth audit corrects the prior count: {c['FULL_TEXT_VERIFIED']} full-text-verified, {c['GOVERNMENT_FULL_SOURCE_VERIFIED']} government, {c['ABSTRACT_RESULT_ONLY']} abstract-result-only, and {c['SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT']} insufficient. Only {len(results)} Result_IDs are source-located; no sentence is readjudicated.\n")
if __name__=='__main__':main()
