"""Batch 10.4F-R1B1D: final retained-reference evidence-packet consolidation.
This is an availability/traceability build only; it does not adjudicate sentence support.
"""
import csv, hashlib, json
from collections import defaultdict, Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]; O=R/'batch10_4f_r1b1d'

def rd(path):
    with path.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def wr(path,fields,rows):
    path.parent.mkdir(exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def unique(rows,key):
    vals=[x[key] for x in rows]
    assert len(vals)==len(set(vals)),f'duplicate {key}'
def main():
    inv=rd(R/'batch10_4f_r1b1'/'FINAL_16_REFERENCE_SOURCE_INVENTORY.csv')
    old=rd(R/'batch10_4f_r1b1'/'RESULT_LEVEL_EVIDENCE_LEDGER.csv')
    abst=rd(R/'batch10_4f_r1b1a'/'NEW_RESULT_LEVEL_EVIDENCE_LEDGER.csv')
    new=rd(R/'batch10_4f_r1b1c'/'NEW_RESULT_LEVEL_EVIDENCE_LEDGER.csv')
    guidance=rd(R/'batch10_4f_r1b1c'/'EV1477_GUIDANCE_EXTRACTION.csv')
    v3=rd(R/'batch10_4f_r1b1c'/'REFERENCE_PACKET_STATUS_V3.csv')
    adj=rd(R/'batch10_4f_r1b'/'SENTENCE_SUPPORT_ADJUDICATION.csv')
    old_rows=[]
    for x in old:
        old_rows.append(dict(Evidence_ID=x['Evidence_ID'],Result_ID=x['Result_ID'],Result_Class='EMPIRICAL_RESULT' if x['Null_Result']!='YES' else 'EMPIRICAL_NULL_RESULT',Source_URL='Prior verified PMC/PubMed source—see upstream provenance',PDF_Page=x['Page_Number'],Source_Locator=f"{x['Source_Section']}; {x['Paragraph_or_Locator']}; {x['Table_Number']}",Study_Design_or_Source_Type='See source-specific upstream packet',Population=x['Population'],Sample=x['Sample_Size'],Setting='See upstream packet',Exposure_or_Intervention=x['Exposure_or_Intervention'],Outcomes=x['Outcome'],Exact_Result=x['Effect_Estimate'],Null_or_Contradictory=x['Null_Result'],Permitted_Claim_Scope='Only source-located result bounded by documented design, population and outcome.',Prohibited_Inference='No causal, universal-readiness, national-prevalence or cross-population inference.',Transferability=x['Transferability_Limitation']))
    abs_rows=[]
    for x in abst:
        abs_rows.append(dict(Evidence_ID=x['Evidence_ID'],Result_ID=x['Result_ID'],Result_Class='ABSTRACT_RESULT',Source_URL='PubMed structured abstract—see upstream provenance',PDF_Page='NR_ABSTRACT',Source_Locator=x['Source_Locator'],Study_Design_or_Source_Type='Abstract-only; no unreported design inferred',Population=x['Population'],Sample='NR',Setting='NR',Exposure_or_Intervention='NR',Outcomes='Structured abstract result',Exact_Result=x['Result_Summary'],Null_or_Contradictory='NR',Permitted_Claim_Scope=x['Permitted_Scope'],Prohibited_Inference=x['Prohibited_Inference'],Transferability='Abstract-only; no unreported transferability inferred.'))
    all_results=old_rows+abs_rows+new
    unique(all_results,'Result_ID')
    by_ev=defaultdict(list)
    for x in all_results:
        assert x['Source_Locator'] and x['PDF_Page']
        by_ev[x['Evidence_ID']].append(x)
    g_by_ev=defaultdict(list)
    for x in guidance:g_by_ev[x['Evidence_ID']].append(x)
    unique(guidance,'Guidance_ID')
    assert not set(x['Guidance_ID'] for x in guidance)&set(x['Result_ID'] for x in all_results)
    source_depth={x['Evidence_ID']:x['Source_Depth'] for x in v3}
    assert Counter(source_depth.values())==Counter({'FULL_TEXT_VERIFIED':7,'GOVERNMENT_FULL_SOURCE_VERIFIED':1,'ABSTRACT_RESULT_ONLY':2,'SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT':6})
    depth_label={'FULL_TEXT_VERIFIED':'FULL_TEXT_RESULT_READY','GOVERNMENT_FULL_SOURCE_VERIFIED':'GOVERNMENT_GUIDANCE_READY','ABSTRACT_RESULT_ONLY':'ABSTRACT_RESULT_READY','SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT':'SOURCE_INSUFFICIENT'}
    packet_label={'FULL_TEXT_VERIFIED':'PACKET_COMPLETE_RESULT_LEVEL','GOVERNMENT_FULL_SOURCE_VERIFIED':'PACKET_COMPLETE_GUIDANCE_LEVEL','ABSTRACT_RESULT_ONLY':'PACKET_COMPLETE_ABSTRACT_LEVEL','SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT':'PACKET_COMPLETE_SOURCE_INSUFFICIENT'}
    final=[]; depth=[]; stat=[]; scope=[]; prohibited=[]; transfer=[]; cohort=[]; insuff=[]
    for x in inv:
        ev=x['Evidence_ID']; sd=source_depth[ev]; rids=';'.join(y['Result_ID'] for y in by_ev[ev]) or 'NONE'; gids=';'.join(y['Guidance_ID'] for y in g_by_ev[ev]) or 'NONE'
        loc=' | '.join(f"{y['Result_ID']}: {y['Source_Locator']} ({y['PDF_Page']})" for y in by_ev[ev]) or (' | '.join(f"{y['Guidance_ID']}: {y['Locator']} (PDF p.{y['PDF_Page']})" for y in g_by_ev[ev]) or 'NONE')
        permits=' | '.join(dict.fromkeys(y.get('Permitted_Claim_Scope',y.get('Permitted_Boundary',y.get('Permitted_Scope',y.get('Permitted_Use','NR')))) for y in (by_ev[ev] or g_by_ev[ev]))) or 'No result-level scientific support.'
        forbids=' | '.join(dict.fromkeys(y.get('Prohibited_Inference',y.get('Prohibited_Use','NR')) for y in (by_ev[ev] or g_by_ev[ev]))) or 'No result-level scientific support.'
        trans=' | '.join(dict.fromkeys(y.get('Transferability','Guidance context limited to official scope.') for y in (by_ev[ev] or g_by_ev[ev]))) or 'No source-level transferability assessment possible.'
        cf='CF-BR-PMES-CFO-2023-01' if ev in {'EV-1473','EV-1474'} else 'NO_KNOWN_SHARED_COHORT_IN_CURRENT_PACKET'
        same='YES' if ev in {'EV-1473','EV-1474'} else 'NO'
        identity='PMC3382270_REJECTED_LEGACY_IDENTITY; EV1474_PUBLISHER_IDENTITY_PASS' if ev=='EV-1474' else 'NOT_APPLICABLE_OR_UNCHANGED'
        stype={'FULL_TEXT_VERIFIED':'Verified primary full text','GOVERNMENT_FULL_SOURCE_VERIFIED':'Official government guidance','ABSTRACT_RESULT_ONLY':'PubMed structured abstract','SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT':'No result-level source in frozen scope'}[sd]
        row=dict(Reference_Number=x['Reference_Number'],Reference_ID=x['Reference_ID'],Evidence_ID=ev,Exact_Title=x['Exact_Title'],DOI=x['DOI'],PMID=x['PMID'],PMCID=x['PMCID'],Source_Depth=depth_label[sd],Source_Type=stype,Identity_Status=identity,Study_Design_or_Source_Type=' | '.join(dict.fromkeys(y.get('Study_Design_or_Source_Type',y.get('Study_Design','NR')) for y in by_ev[ev])) or stype,Population=' | '.join(dict.fromkeys(y.get('Population','NR') for y in by_ev[ev])) or 'NR',Sample=' | '.join(dict.fromkeys(y.get('Sample',y.get('Sample_Size','NR')) for y in by_ev[ev])) or 'NR',Setting=' | '.join(dict.fromkeys(y.get('Setting','NR') for y in by_ev[ev])) or 'NR',Exposure_or_Intervention=' | '.join(dict.fromkeys(y.get('Exposure_or_Intervention','NR') for y in by_ev[ev])) or 'NR',Outcomes=' | '.join(dict.fromkeys(y.get('Outcomes',y.get('Outcome','NR')) for y in by_ev[ev])) or ('Official operational guidance; no empirical outcome' if gids!='NONE' else 'NR'),Result_IDs=rids,Guidance_IDs=gids,Null_Result_IDs='NONE',Permitted_Claim_Scope=permits,Prohibited_Inference=forbids,Transferability=trans,Cohort_Family=cf,SAME_COHORT_FAMILY=same,Independent_Cohort_Count='1' if same=='YES' else 'NR',Source_Locators=loc,Packet_Status=packet_label[sd])
        final.append(row)
        depth.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Source_Depth':depth_label[sd]})
        stat.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Packet_Status':packet_label[sd]})
        scope.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Permitted_Claim_Scope':permits})
        prohibited.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Prohibited_Inference':forbids})
        transfer.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Transferability':trans})
        cohort.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Cohort_Family':cf,'SAME_COHORT_FAMILY':same,'Independent_Cohort_Count':row['Independent_Cohort_Count'],'Rule':'Do not treat EV-1473 and EV-1474 as independent replications.' if same=='YES' else 'No same-cohort relationship documented in this packet.'})
        if sd=='SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT':
            insuff.append({'Reference_ID':x['Reference_ID'],'Evidence_ID':ev,'Current_Citation_Uses':f"International {x['International_Use']}; Brazil {x['Brazil_Use']}",'Result_Level_Support_Available':'NO','Contextual_or_Methods_Use_May_Remain':'PENDING R1B2 SOURCE-LEVEL READJUDICATION','Risk_If_Current_Claim_Depends_On_It':'Claim may require narrowing, citation change or deletion.','Status':'PACKET_COMPLETE_SOURCE_INSUFFICIENT'})
    # Null record IDs, plus the partial-null component embedded in EV-1474-R01.
    null=[]
    for r in all_results:
        if r['Null_or_Contradictory']=='YES' or r.get('Result_Class')=='EMPIRICAL_NULL_RESULT':null.append({'Evidence_ID':r['Evidence_ID'],'Result_ID':r['Result_ID'],'Null_Status':'NULL_RESULT_PRESERVED','Locator':r['Source_Locator'],'Note':'Retained without suppression.'})
    null.append({'Evidence_ID':'EV-1474','Result_ID':'EV-1474-R01','Null_Status':'PARTIAL_NULL_COMPONENT_PRESERVED','Locator':'Table 3; correlation matrix','Note':'Most other anthropometric correlations in the same table were non-significant; result remains association-plus-null context.'})
    null.append({'Evidence_ID':'EV-1479','Result_ID':'EV-1479-R01','Null_Status':'NULL_RESULT_PRESERVED','Locator':'Results, Table 4 and first Results interpretation paragraph on p.16','Note':'No statistically significant program-effect coefficient for the listed outcomes.'}) if not any(x['Result_ID']=='EV-1479-R01' for x in null) else None
    # De-duplicate null ledger by Result_ID/status pair while retaining EV1474 partial notation.
    seen=set(); null=[x for x in null if not ((x['Result_ID'],x['Null_Status']) in seen or seen.add((x['Result_ID'],x['Null_Status'])))]
    null_ids={x['Result_ID'] for x in null if x['Null_Status']=='NULL_RESULT_PRESERVED'}
    for row in final:row['Null_Result_IDs']=';'.join(sorted(x for x in null_ids if x.startswith(row['Evidence_ID']))) or 'NONE'
    # Crosswalk evaluates availability only; no sentence support determination is made.
    cross=[]
    for s in adj:
        evs=[e for e in s['Evidence_ID'].split(';') if e]
        rids=[r['Result_ID'] for e in evs for r in by_ev[e]]
        gids=[g['Guidance_ID'] for e in evs for g in g_by_ev[e]]
        depths=[depth_label[source_depth[e]] for e in evs]
        if rids and any(source_depth[e]=='FULL_TEXT_VERIFIED' for e in evs if by_ev[e]): avail='RESULTS_AVAILABLE'
        elif gids:avail='GUIDANCE_AVAILABLE'
        elif rids:avail='ABSTRACT_RESULT_AVAILABLE'
        else:avail='NO_RESULT_LEVEL_SOURCE'
        cross.append({'Sentence_ID':s['Sentence_ID'],'Existing_Reference_ID':s['Reference_ID'],'Available_Result_IDs':';'.join(rids) or 'NONE','Available_Guidance_IDs':';'.join(gids) or 'NONE','Source_Depth':';'.join(depths) or 'NO_CITED_REFERENCE','Candidate_Result_Availability':avail,'Sentence_Support_Adjudication':'NOT_PERFORMED_IN_R1B1D'})
    assert len(cross)==168
    changes=[]; nar=[]
    for s,c in zip(adj,cross):
        if s['Final_Disposition']=='CITATION_CHANGE_REQUIRED':changes.append(dict(Sentence_ID=s['Sentence_ID'],Existing_Reference_ID=c['Existing_Reference_ID'],Candidate_Result_Availability=c['Candidate_Result_Availability'],Available_Result_IDs=c['Available_Result_IDs'],Available_Guidance_IDs=c['Available_Guidance_IDs'],Decision='AVAILABILITY_ONLY—NO_CITATION_CHANGE_DECIDED'))
        if s['Final_Disposition']=='NARROWING_REQUIRED':nar.append(dict(Sentence_ID=s['Sentence_ID'],Existing_Reference_ID=c['Existing_Reference_ID'],Source_Level_Evidence_Available='YES' if c['Candidate_Result_Availability']!='NO_RESULT_LEVEL_SOURCE' else 'NO',Potentially_Relevant_Result_IDs=c['Available_Result_IDs'],Protected_Claim_Category='UNRESOLVED_CONTRADICTORY_EVIDENCE—LIMITATION_REQUIRED',Source_Insufficiency_Persists='YES' if 'SOURCE_INSUFFICIENT' in c['Source_Depth'] else 'NO',Decision='AVAILABILITY_ONLY—NO_TEXT_REWRITE_DECIDED'))
    assert len(changes)==147 and len(nar)==21
    # outputs
    wr(O/'FINAL_16_REFERENCE_EVIDENCE_PACKETS.csv',list(final[0]),final)
    wr(O/'FINAL_RESULT_LEVEL_EVIDENCE_LEDGER.csv',list(all_results[0]),all_results)
    loc=[{k:r[k] for k in ['Evidence_ID','Result_ID','Source_URL','PDF_Page','Source_Locator','Result_Class']} for r in all_results];wr(O/'FINAL_RESULT_SOURCE_LOCATORS.csv',list(loc[0]),loc)
    wr(O/'FINAL_GUIDANCE_LEDGER.csv',list(guidance[0]),guidance);wr(O/'FINAL_SOURCE_DEPTH_STATUS.csv',list(depth[0]),depth);wr(O/'FINAL_PACKET_STATUS.csv',list(stat[0]),stat);wr(O/'FINAL_PERMITTED_CLAIM_SCOPE.csv',list(scope[0]),scope);wr(O/'FINAL_PROHIBITED_INFERENCE.csv',list(prohibited[0]),prohibited);wr(O/'FINAL_TRANSFERABILITY_STATUS.csv',list(transfer[0]),transfer);wr(O/'FINAL_NULL_RESULT_LEDGER.csv',list(null[0]),null);wr(O/'FINAL_COHORT_RELATIONSHIP.csv',list(cohort[0]),cohort);wr(O/'FINAL_SOURCE_INSUFFICIENT_STATUS.csv',list(insuff[0]),insuff);wr(O/'SENTENCE_RESULT_CANDIDATE_CROSSWALK_V4.csv',list(cross[0]),cross);wr(O/'CITATION_CHANGE_SOURCE_COVERAGE_FINAL.csv',list(changes[0]),changes);wr(O/'NARROWING_SOURCE_COVERAGE_FINAL.csv',list(nar[0]),nar)
    identity=rd(R/'batch10_4f_r1b1c'/'EV1474_PUBLISHER_IDENTITY_VALIDATION.csv');wr(O/'EV1474_IDENTITY_FINAL.csv',list(identity[0]),identity)
    outputs=[p for p in O.iterdir() if p.suffix=='.csv']
    manifest={'batch':'BATCH 10.4F-R1B1D','gate':'EVIDENCE_PACKET_CONSOLIDATION_PASS','reference_packets_finalized':'16/16','full_text_result_ready':'7/16','government_guidance_ready':'1/16','abstract_result_ready':'2/16','source_insufficient':'6/16','empirical_result_ids_total':11,'abstract_result_ids_total':2,'non_empirical_context_result_ids_total':2,'guidance_ids_total':len(guidance),'result_ids_total':len(all_results),'result_ids_with_locator':f'{len(all_results)}/{len(all_results)}','permitted_claim_scopes_complete':'16/16','prohibited_inference_complete':'16/16','transferability_complete':'16/16','cohort_relationship_complete':'16/16','null_result_ids_preserved':len(null_ids),'null_result_suppression':0,'sentence_crosswalk_rows':'168/168','citation_change_coverage_rows':'147/147','narrowing_coverage_rows':'21/21','forced_support_decisions':0,'sentence_readjudication':0,'manuscript_changes':0,'zotero_changes':0,'cef_v1_changes':0,'EV1474_identity':'EV1474_PUBLISHER_IDENTITY_PASS','EV1474_legacy_pmcid':'PMC3382270_REJECTED_LEGACY_IDENTITY','deterministic_regeneration':'python analysis/build_batch10_4f_r1b1d.py','artifact_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}}
    (O/'BATCH10_4F_R1B1D_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=f'''# BATCH 10.4F-R1B1D — final evidence packet consolidation

## Gate

`EVIDENCE_PACKET_CONSOLIDATION_PASS`

`GO_SENTENCE_SUPPORT_READJUDICATION_R1B2`

All **16/16** reference packets now have exactly one final source-depth state and one packet status. This is a traceability consolidation, not sentence support adjudication.

| Final state | Count |
|---|---:|
| `FULL_TEXT_RESULT_READY` | 7/16 |
| `GOVERNMENT_GUIDANCE_READY` | 1/16 |
| `ABSTRACT_RESULT_READY` | 2/16 |
| `SOURCE_INSUFFICIENT` | 6/16 |

## Result and guidance integrity

- **15/15** unique Result_IDs have a source locator; 11 are empirical, 2 abstract-level, and 2 explicitly non-empirical/contextual.
- **2/2** unique Guidance_IDs belong only to EV-1477 and are not empirical results.
- Four pure null-result IDs are retained, plus the partial-null component documented within EV-1474-R01. `NULL_RESULT_SUPPRESSION = 0`.
- EV-1473 and EV-1474 remain `CF-BR-PMES-CFO-2023-01`, independent cohort count 1.
- EV-1474 is publisher/DOI/PMID reconciled; `PMC3382270_REJECTED_LEGACY_IDENTITY` is retained in the final packet.

## Source-insufficient packets

Six packets are closed as insufficient: EXT-TFF-2013, EXT-ACC-AHA-2026, EV-1472, EV-1478, EV-1480, and EV-1483. They are not removed or recovered here. The next R1B2 gate must decide, at sentence level, whether each current use is narrowed, changed, deleted, or retained as non-evidentiary context.

## Sentence availability only

The V4 crosswalk has **168/168** rows. Its coverage derivatives contain **147/147** citation-change rows and **21/21** narrowing rows. They state only source/result availability; no support fit, citation replacement, text rewrite, claim freeze, or reference decision was made.

## Guardrails

No manuscript, Zotero, CEF-v1, reference set, or sentence-adjudication decision was changed. The build is deterministic and all source insufficiencies remain explicit.
'''
    (O/'BATCH10_4F_R1B1D_REPORT.md').write_text(report,encoding='utf-8')
if __name__=='__main__':main()
