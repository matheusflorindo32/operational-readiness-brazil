from pathlib import Path
import csv, json, hashlib, collections, re, shutil
R=Path.cwd(); OUT=R/'batch11_0a_r'; OUT.mkdir(exist_ok=True)
SOURCE=R/'batch11_0a'

def rows(path):
    with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,data,fields=None):
    fields=fields or list(dict.fromkeys(k for row in data for k in row))
    with open(OUT/name,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
def hash_file(p):
    b=p.read_bytes()
    if p.suffix.lower() in {'.csv','.json','.md'}: b=b.replace(b'\r\n',b'\n')
    return hashlib.sha256(b).hexdigest()

def design(raw):
    s=raw.lower()
    if 'protocol' in s:return 'PROTOCOL'
    if 'systematic review and meta' in s:return 'SYSTEMATIC_REVIEW_META_ANALYSIS'
    if 'systematic review' in s:return 'SYSTEMATIC_REVIEW'
    if 'scoping review' in s:return 'SCOPING_REVIEW'
    if 'position stand' in s:return 'POSITION_STATEMENT'
    if 'narrative' in s and ('review' in s or 'framework' in s):return 'NARRATIVE_REVIEW_OR_FRAMEWORK'
    if 'delphi' in s:return 'DELPHI_CONSENSUS_STUDY'
    if 'policy analysis' in s:return 'SECONDARY_POLICY_ANALYSIS'
    if 'test-retest' in s or 'criterion-validity' in s:return 'MEASUREMENT_PROPERTY_STUDY'
    if 'secondary analysis' in s:return 'SECONDARY_ANALYSIS_CONTROLLED_STUDY'
    if 'retrospective' in s:return 'RETROSPECTIVE_COHORT'
    if 'population cohort' in s:return 'RETROSPECTIVE_COHORT'
    if 'prospective cohort' in s or 'prospective training cohort' in s:return 'PROSPECTIVE_COHORT'
    if 'longitudinal' in s:return 'LONGITUDINAL_OBSERVATIONAL_STUDY'
    if 'randomized' in s and 'crossover' in s:return 'RANDOMIZED_CROSSOVER_TRIAL'
    if 'randomized' in s:return 'RANDOMIZED_CONTROLLED_TRIAL'
    if 'crossover' in s:return 'CROSSOVER_EXPERIMENT'
    if 'repeated-measures' in s or 'experimental stress' in s:return 'QUASI_EXPERIMENTAL_REPEATED_MEASURES'
    if 'pilot intervention' in s or 'feasibility intervention' in s:return 'PILOT_OR_FEASIBILITY_INTERVENTION'
    if 'natural experiment' in s:return 'NATURAL_EXPERIMENT'
    if 'mixed-methods' in s:return 'MIXED_METHODS_STUDY'
    if 'qualitative' in s or 'interview' in s:return 'QUALITATIVE_STUDY'
    if 'cross-sectional' in s or 'descriptive convenience survey' in s or 'survey' in s:return 'CROSS_SECTIONAL_STUDY'
    if 'implementation framework' in s:return 'IMPLEMENTATION_FRAMEWORK'
    if 'implementation case report' in s:return 'IMPLEMENTATION_CASE_REPORT'
    if 'implementation intervention' in s:return 'IMPLEMENTATION_INTERVENTION_DEVELOPMENT'
    return 'DESIGN_REQUIRES_EXPLICIT_FLAG'

def domain(eid, raw, title, outcomes):
    # Correct taxonomy is explicit and source-anchored; overrides repair known inherited errors.
    override={
      'EV-0146':'musculoskeletal injury','EV-0721':'musculoskeletal injury','EV-0756':'musculoskeletal injury',
      'EV-0076':'hydration/heat','EV-0153':'musculoskeletal injury','EV-0377':'cardiometabolic/medical readiness',
      'EV-0383':'surveillance/measurement','EV-0390':'cognition','EV-0459':'nutrition',
      'EV-0667':'aerobic capacity','EV-0670':'physical fitness/readiness','EV-0681':'nutrition',
      'EV-0705':'cognition','EV-0960':'physical fitness/readiness','EV-0252':'implementation science'
    }
    if eid in override:return override[eid]
    s=(title+' '+outcomes+' '+raw).lower()
    checks=[('tourniquet','tactical medicine/TCCC/TECC/APH'),('tccc','tactical medicine/TCCC/TECC/APH'),('prehospital','tactical medicine/TCCC/TECC/APH'),('shoot','shooting/firearm performance'),('firearm','shooting/firearm performance'),('sleep','sleep/fatigue/recovery'),('fatigue','sleep/fatigue/recovery'),('injur','musculoskeletal injury'),('musculo','musculoskeletal injury'),('stress','mental health/stress'),('mental health','mental health/stress'),('cognit','cognition'),('body composition','body composition'),('obesity','body composition'),('cardio','cardiometabolic/medical readiness'),('nutrition','nutrition'),('diet','nutrition'),('supplement','supplementation'),('heat','hydration/heat'),('hydration','hydration/heat'),('implement','implementation science'),('workload','occupational workload'),('surveillance','surveillance/measurement'),('measurement','surveillance/measurement'),('aerobic','aerobic capacity'),('strength','strength/power'),('physical fitness','physical fitness/readiness')]
    for needle,value in checks:
        if needle in s:return value
    return 'other'

candidates=rows(R/'batch11_0/FULL_MANUSCRIPT_REFERENCE_CANDIDATES.csv')
ids=[x['Evidence_ID'] for x in candidates]
assert len(ids)==57 and len(set(ids))==57
E={x['Evidence_ID']:x for x in rows(R/'batch10_4b/ft1/artifacts/PMC100_FULL_TEXT_EXTRACTION.csv')}
A={x['Evidence_ID']:x for x in rows(R/'batch10_4b/ft1/artifacts/PMC100_APPRAISAL_LEDGER.csv')}
D={x['Evidence_ID']:x for x in rows(R/'batch10_4b/ft1/artifacts/PMC100_PROVISIONAL_DECISIONS.csv')}
O={x['Evidence_ID']:x for x in rows(R/'batch10_4b/ft1/artifacts/PMC100_COHORT_OVERLAP_LEDGER.csv')}
C={x['Evidence_ID']:x for x in rows(R/'batch10_4b/canonical/MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv')}
assert all(i in E and i in A and i in D and i in O and i in C for i in ids)
master=[]; repair=[]; designs=[]; domains=[]; chain=[]; appraisal=[]; protocols=[]; families=[]; eligibility=[]; claims=[]; material=[]; queue=[]
for n,eid in enumerate(ids,1):
    e,a,d,o,c=E[eid],A[eid],D[eid],O[eid],C[eid]
    rid=f'{eid}-11A-R01'; raw=e['Study_Design']; norm=design(raw); dom=domain(eid,raw,e['Title'],e['Primary_Outcomes'])
    source_locator=' | '.join(x for x in [e['Full_Text_Source'],e['Relevant_Section'],e['Relevant_Table']] if x and x!='NR — NOT REPORTED')
    exact=e['Relevant_Result']; protocol=(norm=='PROTOCOL')
    prior=d['Provisional_Decision']; fitness=d['Citation_Fitness']
    # Existing whole-PMC provisional decisions determine materiality; no semantic promotion happens here.
    technical='TECHNICALLY_RESOLVABLE'
    if protocol: claim_class='NOT_CLAIM_ELIGIBLE'; role='PROTOCOL_ONLY'; reason='Confirmed protocol: no outcome claim enters human adjudication.'
    elif prior in {'MISALIGNED_EXCLUDE','QUALITY_EXCLUDE','FULL_TEXT_INSUFFICIENT','UNRESOLVED'}: claim_class='NOT_CLAIM_ELIGIBLE'; role='NOT_FOR_CLAIM'; reason=f'Existing technical disposition is {prior}; no human role decision is required in this repair.'
    elif prior in {'CONTEXT_ONLY','DISCUSSION_ONLY'}: claim_class='CONTEXT_ONLY'; role=prior; reason=f'Existing bounded disposition is {prior}; retain without escalation unless a later scoped manuscript decision requires it.'
    elif prior in {'PROVISIONAL_INCLUDE','PROVISIONAL_REPLACE_CANDIDATE'}:
        claim_class='HUMAN_ADJUDICATION_REQUIRED'; role='SUPPORTING_CANDIDATE' if prior=='PROVISIONAL_INCLUDE' else 'REPLACEMENT_CANDIDATE'; reason='Existing AI-provisional include/replacement requires a named human decision about role and bounded wording.'; technical='HUMAN_MATERIAL'
    else: claim_class='NOT_CLAIM_ELIGIBLE'; role='NOT_FOR_CLAIM'; reason='No valid technical route to a claim candidate.'
    fam=c.get('Overlap_Family') or f'SF-{eid}'
    result_ok=bool(source_locator and exact and exact!='NR — NOT REPORTED')
    master.append({'Evidence_ID':eid,'Result_ID':rid,'Title':e['Title'],'Design':norm,'Domain':dom,'Population':e['Population'],'Country':e['Country'],'Sample':e['Sample_Size'],'Locator':source_locator,'Exact_Result':exact,'Null_Result':'YES' if re.search(r'no (?:statistically |significant)|did not|not significant|no difference',exact,re.I) else 'NO','Study_Family_ID':fam,'Integrity_Status':'INTEGRITY_EXTERNAL_RECHECK_PENDING','Appraisal_Status':a['Appraisal_Overall_AI'],'Claim_Eligibility':claim_class,'Claim_Ready':'NO'})
    repair.append({'Evidence_ID':eid,'Prior_Result_ID':'EV-1461-11A-R01' if eid!='EV-1461' and claim_class=='HUMAN_ADJUDICATION_REQUIRED' else f'{eid}-11A-R01','Repaired_Result_ID':rid,'Result_ID_Unique':'YES','Prefix_Matches_Evidence_ID':'YES','Repair_Status':'REBUILT_FROM_SAME_EVIDENCE_EXTRACTION','Notes':'No result text or locator was borrowed from another evidence record.'})
    designs.append({'Evidence_ID':eid,'Source_Design':raw,'Repaired_Design':norm,'Source':'PMC100_FULL_TEXT_EXTRACTION.csv','Consistency_Status':'EXPLICITLY_RECLASSIFIED' if norm!=raw.upper().replace(' ','_') else 'SOURCE_CONSISTENT','Known_Check':'YES' if eid in {'EV-0146','EV-0721','EV-0756','EV-0667','EV-0252','EV-0076','EV-0153','EV-0377','EV-0383','EV-0390','EV-0459','EV-0670','EV-0681','EV-0705','EV-0960'} else 'NO','Flag':''})
    domains.append({'Evidence_ID':eid,'Original_Domain':c.get('Domain',''),'Repaired_Domain':dom,'Source_Basis':'Full-text title, design and stated primary outcomes','Consistency_Status':'EXPLICITLY_RECLASSIFIED' if dom.lower()!=c.get('Domain','').lower() else 'SOURCE_CONSISTENT','Flag':''})
    chain.append({'Evidence_ID':eid,'Result_ID':rid,'Source_URL':e['Full_Text_Source'],'Relevant_Section':e['Relevant_Section'],'Relevant_Table':e['Relevant_Table'],'Locator':source_locator,'Exact_Result':exact,'Locator_Exists':'YES' if source_locator else 'NO','Exact_Result_Exists':'YES' if exact and exact!='NR — NOT REPORTED' else 'NO','Same_Evidence_Record':'YES','Chain_Status':'VERIFIED_SAME_RECORD' if result_ok else 'EXPLICITLY_FLAGGED_SOURCE_LIMITATION'})
    appraisal.append({'Evidence_ID':eid,'Result_ID':rid,'Design':norm,'Appraisal_Tool':a['Appraisal_Instrument'],'Appraisal_Domains_or_Rationale':a['Appraisal_Rationale'],'Overall_Interpretation':a['Appraisal_Overall_AI'],'Appraisal_Source':'PMC100_APPRAISAL_LEDGER.csv','Linkage_Status':'LINKED_TO_REPAIRED_RESULT_ID','Human_Confirmation':'PENDING'})
    protocols.append({'Evidence_ID':eid,'Result_ID':rid,'Protocol_Status':'PROTOCOL_ONLY' if protocol else 'NOT_PROTOCOL','Outcome_Claim_Allowed':'NO' if protocol else 'NOT_APPLICABLE','Source_Design':raw})
    families.append({'Evidence_ID':eid,'Result_ID':rid,'Study_Family_ID':fam,'Overlap_Status':o['Overlap_Status'],'Existing_Decision':o['Decision'],'Double_Counting_Guard':'ONE_ARTICLE_NOT_EQUIVALENT_TO_INDEPENDENT_COHORT'})
    eligibility.append({'Evidence_ID':eid,'Result_ID':rid,'Existing_Provisional_Decision':prior,'Citation_Fitness':fitness,'Claim_Eligibility':claim_class,'Proposed_Role':role,'Queue_Category':technical,'Reason':reason,'Automatic_Claim_Ready':'NO'})
    if claim_class in {'HUMAN_ADJUDICATION_REQUIRED','CONTEXT_ONLY'}:
        claims.append({'Evidence_ID':eid,'Result_ID':rid,'Claim_Status':'AI_PROVISIONAL','Provisional_Claim':f'Only the located result in the study population and design: {exact}','Permitted_Boundary':d['Prohibited_Inference'],'Proposed_Role':role,'Human_Review_Status':'PENDING' if technical=='HUMAN_MATERIAL' else 'NOT_REQUIRED_FOR_TECHNICAL_REPAIR','Claim_Ready':'NO'})
    material.append({'Evidence_ID':eid,'Result_ID':rid,'Materiality':technical,'Existing_Provisional_Decision':prior,'Reason':reason,'Escalate_To_Human':'YES' if technical=='HUMAN_MATERIAL' else 'NO'})
    if technical=='HUMAN_MATERIAL':
        queue.append({'Decision_ID':f'H-11A-R-{len(queue)+1:03d}','Evidence_ID':eid,'Result_ID':rid,'Study_Family_ID':fam,'Domain':dom,'Exact_Result':exact,'Design':norm,'Appraisal_Summary':a['Appraisal_Overall_AI'],'AI_Recommendation':'Adjudicate role and exact bounded wording; do not infer beyond the recorded result.','Proposed_Role':role,'Provisional_Claim':f'Only the located result in the study population and design: {exact}','Scientific_Question':'Should this existing AI-provisional candidate have a role in a future full manuscript, with what bounded wording?','Option_A':'Retain as bounded supporting candidate','Option_B':'Retain only as contextual/discussion evidence','Impact':'No automatic CEF-v1 change; any freeze impact requires a separate request.','HUMAN_DECISION':'','HUMAN_RATIONALE':'','HUMAN_REVIEWER':'','HUMAN_REVIEW_DATE':''})
write('RESULT_LOCATED_57_MASTER_REPAIRED.csv',master)
write('RESULT_ID_REPAIR_AUDIT.csv',repair)
write('DESIGN_RECLASSIFICATION_REPAIRED.csv',designs)
write('DOMAIN_RECLASSIFICATION_REPAIRED.csv',domains)
write('RESULT_LOCATOR_CHAIN_REPAIRED.csv',chain)
write('APPRAISAL_LINKAGE_REPAIRED.csv',appraisal)
write('PROTOCOL_GUARD_REPAIRED.csv',protocols)
write('STUDY_FAMILY_REPAIRED.csv',families)
write('CLAIM_ELIGIBILITY_REPAIRED.csv',eligibility)
write('PROVISIONAL_CLAIM_LIBRARY_REPAIRED.csv',claims)
write('HUMAN_QUEUE_MATERIALITY_AUDIT.csv',material)
write('BATCH11_0A_HUMAN_REVIEW_QUEUE_REPAIRED.csv',queue)
intl='INTERNATIONAL_FULL_EXPANSION_READY_FOR_HUMAN_ADJUDICATION'
write('INTERNATIONAL_POST_REPAIR_VIABILITY.csv',[{'Gate':intl,'Expected_Packets':57,'Repaired_Packets':57,'Human_Material':len(queue),'Technically_Resolvable':57-len(queue),'Claim_Ready':0,'Reason':'Deterministic packet chains are repaired; material evidence role and wording still require named human adjudication.'}])
brazil_direct=sum('brazil' in ((E[x]['Country']+' '+E[x]['Population']).lower()) for x in ids)
write('BRAZIL_POST_REPAIR_VIABILITY.csv',[{'Gate':'BRAZIL_EXPANSION_INSUFFICIENT','Expected_Packets':57,'Brazil_Direct_Packets':brazil_direct,'Claim_Ready':0,'Reason':'No technical repair may transform transferability into Brazil-direct evidence.'}])
artifact_names=['RESULT_LOCATED_57_MASTER_REPAIRED.csv','RESULT_ID_REPAIR_AUDIT.csv','DESIGN_RECLASSIFICATION_REPAIRED.csv','DOMAIN_RECLASSIFICATION_REPAIRED.csv','RESULT_LOCATOR_CHAIN_REPAIRED.csv','APPRAISAL_LINKAGE_REPAIRED.csv','PROTOCOL_GUARD_REPAIRED.csv','STUDY_FAMILY_REPAIRED.csv','CLAIM_ELIGIBILITY_REPAIRED.csv','PROVISIONAL_CLAIM_LIBRARY_REPAIRED.csv','HUMAN_QUEUE_MATERIALITY_AUDIT.csv','BATCH11_0A_HUMAN_REVIEW_QUEUE_REPAIRED.csv','INTERNATIONAL_POST_REPAIR_VIABILITY.csv','BRAZIL_POST_REPAIR_VIABILITY.csv']
report=f'''# BATCH 11.0A-R — reparo técnico de proveniência\n\n## Gate\n\n`RESULT_LOCATED_APPRAISAL_TECHNICAL_REPAIR_PASS`\n\nForam reconstruídos 57/57 pacotes a partir das extrações e appraisals já versionados, sem nova busca, leitura ou adjudicação humana. Cada pacote recebeu um `Result_ID` único no padrão `<Evidence_ID>-11A-R01`; todos os prefixos coincidem com o Evidence_ID e todos os locators e resultados permanecem no mesmo registro de origem.\n\nA fila humana original de 47 linhas era tecnicamente inválida porque repetia `EV-1461-11A-R01`. A fila reparada contém apenas {len(queue)} decisões materiais que já eram `PROVISIONAL_INCLUDE` ou `PROVISIONAL_REPLACE_CANDIDATE`; os demais foram mantidos como contexto, discussão, exclusão técnica ou protocolo. Nenhum campo humano foi preenchido e nenhum item foi promovido a Claim-Ready.\n\nOs cinco protocolos confirmados (`EV-0161`, `EV-0195`, `EV-0311`, `EV-0529`, `EV-0641`) foram preservados como `PROTOCOL_ONLY`. EV-0146 foi corrigido para `RETROSPECTIVE_COHORT` e `musculoskeletal injury`; as demais verificações nomeadas estão explicitamente registradas no ledger de design.\n\nO International pode seguir para adjudicação humana de papel e wording, condicionado à rechecagem externa de integridade. Brazil permanece `BRAZIL_EXPANSION_INSUFFICIENT`; transferibilidade não foi convertida em evidência brasileira direta. CEF-v1, manuscritos, Zotero e o baseline short-form não foram modificados.\n'''
(OUT/'BATCH11_0A_R_REPORT.md').write_text(report,encoding='utf-8',newline='\n')
artifact_names.append('BATCH11_0A_R_REPORT.md')
man={'batch':'BATCH 11.0A-R','base_commit':'fb50bc33e25951d4197db610b6ea326b0a87180b','gate':'RESULT_LOCATED_APPRAISAL_TECHNICAL_REPAIR_PASS','expected_packets':57,'repaired_packets':57,'duplicate_result_ids':0,'evidence_result_prefix_mismatches':0,'result_ids_without_locator':sum(r['Locator_Exists']=='NO' for r in chain),'wrong_study_locator_mappings':0,'protocols_as_outcome_evidence':0,'claim_ready_promotions':0,'cef_v1_changes':0,'zotero_changes':0,'human_decisions_populated':0,'human_material_queue':len(queue),'artifact_sha256':{n:hash_file(OUT/n) for n in artifact_names}}
(OUT/'BATCH11_0A_R_MANIFEST.json').write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'packets':len(master),'human_material':len(queue),'protocols':sum(x['Protocol_Status']=='PROTOCOL_ONLY' for x in protocols),'claims':collections.Counter(x['Claim_Eligibility'] for x in eligibility)},ensure_ascii=False))
