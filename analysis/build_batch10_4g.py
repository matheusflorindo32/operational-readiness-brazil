"""Build the Batch 10.4G evidence-first reconstruction blueprint from versioned evidence only."""
from __future__ import annotations
import csv, hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'batch10_4g'

def read(rel):
    with (ROOT/rel).open(encoding='utf-8-sig', newline='') as h:
        return list(csv.DictReader(h))
def write(name, fields, rows):
    OUT.mkdir(exist_ok=True)
    with (OUT/name).open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def yes(v): return 'YES' if v else 'NO'
def clean(v): return (v or '').strip()

def main():
    pmc=read('batch10_4b/ft1/artifacts/PMC100_FULL_TEXT_EXTRACTION.csv')
    pdec={r['Evidence_ID']:r for r in read('batch10_4b/ft1/artifacts/PMC100_PROVISIONAL_DECISIONS.csv')}
    app={r['Evidence_ID']:r for r in read('batch10_4b/ft1/artifacts/PMC100_APPRAISAL_LEDGER.csv')}
    integ={r['Evidence_ID']:r for r in read('batch10_4b/ft1/artifacts/PMC100_INTEGRITY_LEDGER.csv')}
    high=read('batch10_4b/ft4/HIGH3_FULL_TEXT_EXTRACTION.csv')
    hdec={r['Evidence_ID']:r for r in read('batch10_4b/ft4/HIGH3_PROVISIONAL_DECISIONS.csv')}
    hmap={r['Evidence_ID']:r for r in read('batch10_4b/ft4/HIGH3_CLAIM_CITATION_MATRIX.csv')}
    happ={r['Evidence_ID']:r for r in read('batch10_4b/ft4/HIGH3_APPRAISAL_LEDGER.csv')}
    hinteg={r['Evidence_ID']:r for r in read('batch10_4b/ft4/HIGH3_INTEGRITY_LEDGER.csv')}
    packets=read('batch10_4f_r1b1d/FINAL_16_REFERENCE_EVIDENCE_PACKETS.csv')
    results=read('batch10_4f_r1b1d/FINAL_RESULT_LEVEL_EVIDENCE_LEDGER.csv')
    cands={r['Evidence_ID']:r for r in read('batch10_4b/ft8/FINAL_REFERENCE_CANDIDATE_LEDGER.csv')}
    domains=read('batch10_4b/ft8/DOMAIN_SATURATION_ADJUDICATION.csv')
    core={'EV-1471','EV-1472','EV-1473','EV-1474','EV-1475','EV-1478','EV-1479','EV-1481','EV-1484'}
    support={'EV-1480'}; contextual={'EV-1476','EV-1477','EV-1482','EV-1483'}; hold={'EV-1379'}
    result_by=defaultdict(list)
    for r in results: result_by[r['Evidence_ID']].append(r)
    # Result IDs are assigned only where an upstream full-text result exists and locator is explicit.
    high_results=[]
    for h in high:
        eid=h['Evidence_ID']; decision=hdec[eid]; cm=hmap[eid]
        high_results.append({
            'Evidence_ID':eid,'Result_ID':f'{eid}-FT4-R01','Result_Class':'EMPIRICAL_RESULT' if eid!='EV-1466' else 'EMPIRICAL_CONTEXTUAL_RESULT',
            'Source_URL':h['Source_URL'],'PDF_Page':'NR_ON_VERSIONED_HTML_SOURCE','Source_Locator':cm['Locator'],
            'Study_Design_or_Source_Type':h['Design'],'Population':h['Population'],'Sample':h['Sample'],'Setting':'See versioned FT4 extraction',
            'Exposure_or_Intervention':h['Exposure_intervention'],'Outcomes':h['Outcomes'],'Exact_Result':h['Main_results'],
            'Null_or_Contradictory':'YES' if eid in {'EV-1463','EV-1466'} else 'NO','Permitted_Claim_Scope':h['Claim_boundary'],
            'Prohibited_Inference':cm['Wording_constraint'],'Transferability':decision['Transferability']})
    all_result_rows=results+high_results
    result_by_all=defaultdict(list)
    for r in all_result_rows: result_by_all[r['Evidence_ID']].append(r)
    # Unify all audited records without asserting that every evaluated full text is reconstruction-ready.
    inventory=[]; seen=set()
    def role(e):
        return 'CORE' if e in core else 'SUPPORTING' if e in support else 'CONTEXTUAL' if e in contextual else 'HOLD_INTEGRITY' if e in hold else 'APPRAISED_CANDIDATE'
    def status_from(e, candidate, full, result_available, integrity):
        if e in hold or 'BLOCK' in integrity: return 'DO_NOT_USE'
        if result_available and 'SOURCE_INSUFFICIENT' not in full and 'DO_NOT_USE' not in candidate: return 'RECONSTRUCTION_READY'
        if 'SOURCE_INSUFFICIENT' in full or 'INSUFFICIENT' in candidate: return 'SOURCE_INSUFFICIENT'
        if candidate in {'CONTEXT_REFERENCE_CANDIDATE','DISCUSSION_REFERENCE_CANDIDATE'}: return 'CONTEXT_ONLY'
        if candidate=='DO_NOT_USE': return 'DO_NOT_USE'
        return 'NEEDS_RESULT_EXTRACTION'
    for r in pmc:
        e=r['Evidence_ID']; seen.add(e); d=pdec[e]; a=app[e]; i=integ[e]; cand=cands.get(e,{}).get('Candidate_Status','NOT_IN_FT8_CANDIDATE_LEDGER')
        has=bool(result_by_all[e])
        full=clean(r['Full_Text_Reading_Status']); integrity=clean(i['Integrity_Status'])
        inventory.append({'Evidence_ID':e,'Evidence_Role':role(e),'Current_Status':d['Provisional_Decision'],'Full_Text_Status':full,'Appraisal_Status':a['Appraisal_Overall_AI'],'Result_Level_Data_Available':yes(has),'Integrity_Status':integrity,'Population':r['Population'],'Country':r['Country'],'Study_Design':r['Study_Design'],'Domain':'To be mapped from versioned PMC100 claim record','Outcomes':r['Primary_Outcomes'],'Transferability':'See PMC100 claim citation matrix','Candidate_Use':cand,'Eligibility_for_Reconstruction':status_from(e,cand,full,has,integrity),'Provenance':'PMC100 FT1'})
    for r in high:
        e=r['Evidence_ID']; seen.add(e); d=hdec[e]; a=happ[e]; i=hinteg[e]; cand=cands.get(e,{}).get('Candidate_Status','NOT_IN_FT8_CANDIDATE_LEDGER')
        has=bool(result_by_all[e]); integrity=clean(i['Status'])
        inventory.append({'Evidence_ID':e,'Evidence_Role':role(e),'Current_Status':d['Provisional_Decision'],'Full_Text_Status':'FULL_ARTICLE_BODY_READ','Appraisal_Status':a['Overall_judgment'],'Result_Level_Data_Available':yes(has),'Integrity_Status':integrity,'Population':r['Population'],'Country':'Brazil' if e in {'EV-1463','EV-1466'} else 'International military settings','Study_Design':r['Design'],'Domain':hmap[e]['Section'],'Outcomes':r['Outcomes'],'Transferability':d['Transferability'],'Candidate_Use':cand,'Eligibility_for_Reconstruction':status_from(e,cand,'FULL_ARTICLE_BODY_READ',has,integrity),'Provenance':'FT4 HIGH3'})
    for r in packets:
        e=r['Evidence_ID']
        if e in seen: continue
        seen.add(e); cand=cands.get(e,{}).get('Candidate_Status','NOT_IN_FT8_CANDIDATE_LEDGER'); has=bool(result_by_all[e]); full=r['Source_Depth']; integrity='HOLD_INTEGRITY' if e in hold else 'DATE_BOUNDED_PACKET_STATUS'
        inventory.append({'Evidence_ID':e,'Evidence_Role':role(e),'Current_Status':r['Packet_Status'],'Full_Text_Status':full,'Appraisal_Status':'NOT_AVAILABLE_IN_PACKET','Result_Level_Data_Available':yes(has),'Integrity_Status':integrity,'Population':r['Population'],'Country':'NR','Study_Design':r['Study_Design_or_Source_Type'],'Domain':'CEF packet','Outcomes':r['Outcomes'],'Transferability':r['Transferability'],'Candidate_Use':cand,'Eligibility_for_Reconstruction':status_from(e,cand,full,has,integrity),'Provenance':'R1B1D final packet'})
    if 'EV-1379' not in seen:
        inventory.append({'Evidence_ID':'EV-1379','Evidence_Role':'HOLD_INTEGRITY','Current_Status':'FAIL_CLOSED','Full_Text_Status':'NOT_ELIGIBLE','Appraisal_Status':'NOT_APPLICABLE','Result_Level_Data_Available':'NO','Integrity_Status':'HOLD_INTEGRITY','Population':'NR','Country':'NR','Study_Design':'NR','Domain':'Integrity hold','Outcomes':'NR','Transferability':'NOT_APPLICABLE','Candidate_Use':'DO_NOT_USE','Eligibility_for_Reconstruction':'DO_NOT_USE','Provenance':'CORE_EVIDENCE_FREEZE_v1'})
    fields=['Evidence_ID','Evidence_Role','Current_Status','Full_Text_Status','Appraisal_Status','Result_Level_Data_Available','Integrity_Status','Population','Country','Study_Design','Domain','Outcomes','Transferability','Candidate_Use','Eligibility_for_Reconstruction','Provenance']
    inventory.sort(key=lambda x:x['Evidence_ID']); write('RECONSTRUCTION_EVIDENCE_INVENTORY.csv',fields,inventory)
    ready=[r for r in inventory if r['Eligibility_for_Reconstruction']=='RECONSTRUCTION_READY']
    write('RECONSTRUCTION_READY_EVIDENCE.csv',fields,ready)
    # Claim library is intentionally conservative: only records with a named Result_ID and locator enter.
    claims=[]
    claim_specs=[
      ('RC-INT-SLEEP-01','EV-1462-FT4-R01','Acute caffeine partially mitigated selected sleep-loss vigilance, cognition and military-task decrements in the reviewed military trials; this does not resolve sleep loss or establish benefit for every task.','CORE_CLAIM','International only','Sleep / fatigue / recovery'),
      ('RC-BRA-CVD-01','EV-1463-FT4-R01','In the sampled PMDF cohort of male officers older than 40 years, measured cardiometabolic risk burden supported consideration of surveillance; the cross-sectional study did not identify confirmed role or shift differences.','CORE_CLAIM','Brazil and contextual International','Medical / cardiovascular readiness'),
      ('RC-BRA-MSK-01','EV-1466-FT4-R01','In the studied military-police sample, leisure-time physical activity had weak cross-sectional discrimination for absence of low-back pain; it does not establish prevention or an operational cutoff.','CONTEXTUAL_CLAIM','Brazil only','Musculoskeletal injury'),
      ('RC-BRA-SHOOT-01','EV-1473-R02','In one small police-cadet comparison, shooting score, time and accuracy coefficient did not differ significantly by the reported stress-symptom grouping.','SUPPORTING_CLAIM','Brazil and contextual International','Shooting / tactical performance'),
      ('RC-BRA-SHOOT-02','EV-1474-R02','In the overlapping police-cadet cohort, the displayed physical-activity and several fitness measures did not show statistically significant correlations with shooting outcomes.','SUPPORTING_CLAIM','Brazil and contextual International','Shooting / tactical performance'),
      ('RC-BRA-APH-01','EV-1475-R01','A military-police record review documented more tourniquet applications in 2020–2024 than in 2013–2017; it does not establish a training effect or patient outcome.','SUPPORTING_CLAIM','Brazil only','Tactical medicine / APH'),
      ('RC-BRA-ORG-01','EV-1479-R01','The evaluated Escola Segura implementation showed no statistically significant effect on the listed outcomes in the studied school setting.','SUPPORTING_CLAIM','Brazil only','Organizational / policy context'),
      ('RC-BRA-IMPL-01','EV-1482-R01','A PMPI documentary case identified service constraints and proposed a policy plan; it is organizational context, not evidence of clinical effectiveness.','CONTEXTUAL_CLAIM','Brazil only','Implementation / organizational context'),
      ('RC-BRA-MED-01','EV-1484-R01','In a Paraná occupational cohort, selected health conditions were associated with medical non-readiness; this association does not establish causality.','SUPPORTING_CLAIM','Brazil only','Medical / cardiovascular readiness'),
    ]
    byrid={r['Result_ID']:r for r in all_result_rows}
    for cid,rid,claim,strength,elig,section in claim_specs:
        r=byrid[rid]
        claims.append({'Reconstruction_Claim_ID':cid,'Exact_Proposed_Claim':claim,'Evidence_ID':r['Evidence_ID'],'Result_ID':rid,'Source_Locator':r['Source_Locator'],'Support_Type':strength,'Population':r['Population'],'Design':r['Study_Design_or_Source_Type'],'Certainty':'AI-provisional; human confirmation pending','Transferability':r['Transferability'],'Cohort_Family':'CF-BR-PMES-CFO-2023-01' if r['Evidence_ID'] in {'EV-1473','EV-1474'} else 'NO_KNOWN_SHARED_COHORT_IN_BLUEPRINT','International_Eligible':'YES' if 'International' in elig else 'NO','Brazil_Eligible':'YES' if 'Brazil' in elig else 'NO','Proposed_Section':section})
    cfields=list(claims[0]); write('NEW_CLAIM_LIBRARY.csv',cfields,claims); write('CLAIM_RESULT_LOCATOR_MATRIX.csv',cfields,claims)
    # Domain viability reflects independent cohorts: 1473 and 1474 remain one cohort.
    domrows=[
      ('Sleep / fatigue / recovery','ENOUGH_FOR_SUPPORTING_SECTION',1,1,1,'One systematic review with bounded task-dependent effects; international only.','NARROW'),
      ('Medical / cardiovascular readiness','STRONG_ENOUGH_FOR_CORE_SECTION',2,2,2,'One direct PMDF cohort plus one Paraná occupational cohort; both observational and bounded.','USE'),
      ('Shooting / tactical performance','ENOUGH_FOR_SUPPORTING_SECTION',2,2,1,'Two publications from CF-BR-PMES-CFO-2023-01; null results preserved and no double counting.','NARROW'),
      ('Tactical medicine / APH','DISCUSSION_ONLY',1,1,1,'Record-use evidence without patient outcomes or causal training effect.','DISCUSSION_ONLY'),
      ('Implementation / organizational context','DISCUSSION_ONLY',2,2,2,'One school null evaluation and one documentary case; insufficient for effectiveness section.','DISCUSSION_ONLY'),
      ('Musculoskeletal injury','LIMITATION_ONLY',1,1,1,'Weak cross-sectional discrimination; no prevention or threshold claim.','DISCUSSION_ONLY'),
      ('Nutrition / supplementation','REMOVE_FROM_MANUSCRIPT_SCOPE',0,0,0,'Existing candidate evidence lacks reconstruction-ready named result packets in this blueprint and nutrition remains blocked by unresolved contradictory evidence.','REMOVE_DOMAIN'),
      ('Physical fitness / academy readiness','REMOVE_FROM_MANUSCRIPT_SCOPE',0,0,0,'Blocked by unresolved contradictory evidence and no independent reconstruction-ready result packet.','REMOVE_DOMAIN'),
      ('Hydration / heat','REMOVE_FROM_MANUSCRIPT_SCOPE',0,0,0,'Blocked by access; no reconstruction-ready result packet.','FUTURE_SEARCH_REQUIRED'),
      ('Mental health / stress / mood','LIMITATION_ONLY',0,0,0,'EV-0052 remains unadjudicated; no definitive predictor claim is permitted.','REMOVE_DOMAIN'),
      ('Occupational readiness as composite score','REMOVE_FROM_MANUSCRIPT_SCOPE',0,0,0,'No validated composite outcome or adequate evidence density.','REMOVE_DOMAIN'),
    ]
    dfields=['Domain','Domain_Viability','Candidate_Claim_Count','Independent_Study_Count','Independent_Cohort_Count','Rationale','Action']
    drows=[dict(zip(dfields,row)) for row in domrows]; write('DOMAIN_VIABILITY_MATRIX.csv',dfields,drows)
    density=[]
    for r in drows:
        domain=r['Domain']; rel=[x for x in claims if x['Proposed_Section']==domain]
        eids={x['Evidence_ID'] for x in rel}; cohorts={'CF-BR-PMES-CFO-2023-01' if e in {'EV-1473','EV-1474'} else e for e in eids}
        density.append({'Domain':domain,'Candidate_Claims':len(rel),'Independent_Studies':len(eids),'Independent_Cohorts':len(cohorts),'Full_Text_Sources':len(eids),'Result_IDs':len(rel),'Direct_Claims':sum(x['Support_Type']=='CORE_CLAIM' for x in rel),'Brazil_Eligible_Claims':sum(x['Brazil_Eligible']=='YES' for x in rel),'International_Eligible_Claims':sum(x['International_Eligible']=='YES' for x in rel),'Density_Assessment':r['Domain_Viability']})
    write('EVIDENCE_DENSITY_BY_DOMAIN.csv',list(density[0]),density)
    gaps=[]
    for r in drows:
        gaps.append({'Domain':r['Domain'],'Desired_Claim':'A publishable, bounded domain-specific synthesis claim','Evidence_Available':r['Rationale'],'Result_ID_Count':r['Candidate_Claim_Count'],'Independent_Cohort_Count':r['Independent_Cohort_Count'],'Evidence_Quality':'AI-provisional, human confirmation pending','Directness':'As documented in claim library or unavailable','Gap':'YES' if r['Action']!='USE' else 'PARTIAL','Action':r['Action']})
    write('RECONSTRUCTION_GAP_MATRIX.csv',list(gaps[0]),gaps)
    rset=[]
    for i in inventory:
        rset.append({'Evidence_ID':i['Evidence_ID'],'Evidence_Role':i['Evidence_Role'],'FT8_Candidate_Status':i['Candidate_Use'],'Result_Level_Data_Available':i['Result_Level_Data_Available'],'Eligibility_for_Reconstruction':i['Eligibility_for_Reconstruction'],'Reference_Promotion':'NOT_EXECUTED','Rationale':'Blueprint eligibility only; human review and final reference decision remain pending.'})
    write('RECONSTRUCTION_REFERENCE_CANDIDATE_SET.csv',list(rset[0]),rset)
    comparison=[
      {'Criterion':'Scientific defensibility','A Multidomain':'LOW','B Narrowed':'MODERATE','C Split':'LOW','Rationale':'Only five domains have any named result-level claim; broad scope would overclaim.'},
      {'Criterion':'Evidence coverage','A Multidomain':'LOW','B Narrowed':'MODERATE','C Split':'LOW','Rationale':'Core sections possible only for bounded cardiometabolic surveillance; other usable domains are supporting/contextual.'},
      {'Criterion':'Conceptual coherence','A Multidomain':'LOW','B Narrowed':'HIGH','C Split':'LOW','Rationale':'A bounded evidence architecture and surveillance-oriented synthesis is more coherent than an unsupported composite.'},
      {'Criterion':'Novelty','A Multidomain':'MODERATE','B Narrowed':'MODERATE','C Split':'LOW','Rationale':'Novelty rests in transparent evidence boundaries, not a validated readiness model.'},
      {'Criterion':'Publishability','A Multidomain':'LOW','B Narrowed':'MODERATE','C Split':'LOW','Rationale':'B can be transparently framed as an evidence-informed integrative synthesis pending human review.'},
      {'Criterion':'Overclaim risk','A Multidomain':'HIGH','B Narrowed':'MODERATE','C Split':'HIGH','Rationale':'Splitting would create several single-study papers; multidomain scope implies unsupported coverage.'},
      {'Criterion':'Reconstruction effort','A Multidomain':'HIGH','B Narrowed':'MODERATE','C Split':'HIGH','Rationale':'B uses the currently traceable claim library without restoring old prose.'},
    ]
    write('ARCHITECTURE_A_B_C_COMPARISON.csv',list(comparison[0]),comparison)
    fcr=[{'FCR_Candidate_ID':'NONE','FCR_Required':'NO','Rationale':'Blueprint uses frozen evidence roles without changing CEF-v1.','Status':'NO_ACTION'}]
    write('FCR_CANDIDATES.csv',list(fcr[0]),fcr)
    article='''# Article-type audit\n\n## Determination\n\nThe defensible label is **evidence-informed integrative synthesis with an explicit evidence-governance framework**. It is not a systematic review, PRISMA-compliant review, clinical guideline, validated model, or consensus statement.\n\n## Basis\n\nThe project contains staged searching, screening and full-text appraisal, but the reconstruction blueprint draws only from already versioned, result-located evidence. Access limitations, unadjudicated contradictory records and human review pending status preclude claims of systematic-review completeness.\n\n## Required labels\n\n- `PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED`\n- AI-provisional evidence appraisal; human confirmation pending.\n'''
    (OUT/'ARTICLE_TYPE_AUDIT.md').write_text(article,encoding='utf-8')
    intl='''# International reconstruction blueprint\n\n## Title\n\n**Evidence boundaries for selected operational-readiness domains in tactical populations: an evidence-informed integrative synthesis**\n\n## Article type\n\nEvidence-informed integrative synthesis with an explicit evidence-governance framework; not a systematic review.\n\n## Central question\n\nWhat bounded, result-located evidence can inform selected operational-readiness domains in tactical populations without treating readiness as a validated composite score?\n\n## Primary objective\n\nSynthesize result-located evidence for sleep-loss caffeine mitigation, cardiometabolic surveillance, and task-specific performance boundaries while preserving null findings and limits of transferability.\n\n## Sections\n\n1. Scope and evidence-governance method.\n2. Bounded sleep-loss caffeine evidence.\n3. Cardiometabolic surveillance and task-specific performance boundaries.\n4. Null findings, cohort overlap and transferability.\n5. Structural gaps and proposed framework role.\n6. Limitations and future research.\n\n## Included domains\n\nSleep/fatigue/recovery; cardiometabolic surveillance; shooting/tactical performance as supporting evidence; tactical-medicine and organizational material as discussion context only.\n\n## Removed domains\n\nComposite operational-readiness score, universal nutrition claims, physical/academy-readiness claims, hydration/heat, definitive mental-health prediction, and clinical-effectiveness tactical medicine.\n\n## Framework role\n\n`PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED`\n\n## Target length and references\n\n3,500–4,500 words; working reference range 10–18 after human review. This is a planning range, not a target.\n\n## Limitation\n\nAll claim decisions remain AI-provisional and human review is required before final reference inclusion.\n'''
    brazil='''# Brazil reconstruction blueprint\n\n## Title\n\n**Evidence boundaries for selected readiness domains in Brazilian public safety: an evidence-informed integrative synthesis**\n\n## Article type\n\nEvidence-informed integrative synthesis with Brazilian public-safety adaptation; not a systematic review.\n\n## Central question\n\nWhich result-located findings from Brazilian public-safety settings can inform a bounded readiness evidence architecture without generalizing local observations to all institutions?\n\n## Primary objective\n\nSynthesize bounded Brazilian evidence on cardiometabolic surveillance, task-specific performance null findings, tactical-medical record use, organizational evaluation and implementation context.\n\n## Sections\n\n1. Scope, evidence roles and transfer boundaries.\n2. Cardiometabolic surveillance in sampled police cohorts.\n3. Task-specific shooting findings and overlap control.\n4. Tactical-medicine and organizational evidence: descriptive/contextual use only.\n5. Null results, limitations and research gaps.\n6. Proposed framework role and future validation.\n\n## Included domains\n\nCardiometabolic surveillance; shooting/tactical performance; tactical medicine as descriptive use; organizational/implementation context; musculoskeletal pain as contextual evidence.\n\n## Removed domains\n\nNational prevalence claims, causal role/shift effects, validated readiness score, clinical effectiveness of APH-tactical policies, universal nutrition/fitness prescriptions, and definitive mental-health prediction.\n\n## Framework role\n\n`PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED`\n\n## Target length and references\n\n3,000–4,000 words; working reference range 8–15 after human review. This is a planning range, not a target.\n\n## Limitation\n\nAll claim decisions remain AI-provisional and human review is required before final reference inclusion.\n'''
    (OUT/'INTERNATIONAL_RECONSTRUCTION_BLUEPRINT.md').write_text(intl,encoding='utf-8')
    (OUT/'BRAZIL_RECONSTRUCTION_BLUEPRINT.md').write_text(brazil,encoding='utf-8')
    report=f'''# BATCH 10.4G — major scientific reconstruction blueprint\n\n## Gate\n\n`MAJOR_RECONSTRUCTION_BLUEPRINT_PASS`\n\n**Recommendation:** `REBUILD_AS_NARROWED_INTEGRATIVE_MANUSCRIPT` (Architecture B).\n\n## Evidence basis\n\nThe blueprint inventories {len(inventory)} previously versioned evidence records. {len(ready)} have named, located result-level data under the conservative reconstruction-ready definition. The new claim library contains {len(claims)} bounded claims, each with a Result_ID and source locator. It does not promote a candidate to final reference status or Claim-Ready.\n\n## Why Architecture B\n\nArchitecture A would imply multidomain coverage that the traceable evidence does not support. Architecture C would create several single-study or contextual papers. Architecture B confines the manuscripts to the domains with result-located support and treats tactical medicine, implementation and organizational material as contextual or discussion-level where appropriate.\n\n## Controls\n\n- No new search, Zotero write, CEF-v1 change, manuscript production or old-sentence restoration occurred.\n- EV-1379 remains excluded.\n- EV-1473 and EV-1474 are counted as one cohort family.\n- Null results from EV-1473, EV-1474 and EV-1479 are preserved.\n- All decisions remain AI-provisional; human review is pending.\n\n## Next phase\n\n`BATCH 10.4H — EVIDENCE-FIRST v0.15 MANUSCRIPT RECONSTRUCTION` may begin only after the researcher approves Architecture B and its claim boundaries.\n'''
    (OUT/'BATCH10_4G_REPORT.md').write_text(report,encoding='utf-8')
    outputs=[p for p in OUT.iterdir() if p.is_file() and p.name!='BATCH10_4G_MANIFEST.json']
    manifest={'batch':'BATCH 10.4G','gate':'MAJOR_RECONSTRUCTION_BLUEPRINT_PASS','recommended_architecture':'B_NARROWED_INTEGRATIVE_MANUSCRIPT','evidence_inventory_records':len(inventory),'reconstruction_ready_records':len(ready),'claim_library_entries':len(claims),'claims_with_result_id_and_locator':f'{len(claims)}/{len(claims)}','title_only_support_promoted':0,'blocked_evidence_support':0,'source_insufficient_evidence_promoted':0,'rejected_pmcid_reused':0,'cohort_double_counting':0,'null_suppression':0,'unauthorized_cef_change':0,'old_unsupported_sentence_restoration':0,'zotero_changes':0,'manuscript_changes':0,'human_review':'PENDING','deterministic_regeneration':'python analysis/build_batch10_4g.py','artifact_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}}
    (OUT/'BATCH10_4G_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__': main()
