"""FT8 evidence-layer saturation adjudication; no discovery, appraisal, or manuscript edit."""
from __future__ import annotations
import csv, hashlib, json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4b'/'ft8';OUT.mkdir(parents=True,exist_ok=True)
FT1=ROOT/'batch10_4b'/'ft1'/'artifacts'; FT4=ROOT/'batch10_4b'/'ft4'; FT5=ROOT/'batch10_4b'/'ft5'; FT7=ROOT/'batch10_4b'/'ft7'
DOMAINS=[
('Operational / occupational readiness','PARTIALLY_SATURATED','Operational outcomes are represented but remain heterogeneous across occupations.'),
('Physical / academy readiness','BLOCKED_BY_UNRESOLVED_CONTRADICTORY_EVIDENCE','EV-0052 and EV-1066 remain unadjudicated contradictory HIGH evidence.'),
('Nutrition','BLOCKED_BY_UNRESOLVED_CONTRADICTORY_EVIDENCE','EV-0140 remains unadjudicated contradictory HIGH evidence.'),
('Shift work','PARTIALLY_SATURATED','Existing nutrition/shift coverage is not a standalone shift-work evidence base.'),
('Sleep / fatigue / recovery','PARTIALLY_SATURATED','Bounded FT4 caffeine synthesis is available; directness and transferability remain limited.'),
('Cognition','BLOCKED_BY_ACCESS','Relevant HIGH replacements remain inaccessible.'),
('Firearm / operational performance','PARTIALLY_SATURATED','Coverage exists but direct operational-task outcomes remain incomplete.'),
('Medical / cardiovascular readiness','PARTIALLY_SATURATED','PMDF surveillance is direct but cross-sectional and cohort-specific.'),
('Musculoskeletal injury','PARTIALLY_SATURATED','Substantial provisional coverage exists; causal/prevention inference remains bounded.'),
('Tactical medicine','BLOCKED_BY_ACCESS','P0 HIGH records remain inaccessible.'),
('TCCC / TECC / APH','BLOCKED_BY_ACCESS','P0 HIGH records remain inaccessible.'),
('Implementation science','PARTIALLY_SATURATED','Provisional implementation evidence exists but public-safety institutional directness remains incomplete.'),
('Organizational / policy readiness','NOT_SATURATED','No completed dedicated coverage category.'),
('Hydration / heat','BLOCKED_BY_ACCESS','Only two FT1 records; a P0 HIGH remains inaccessible.'),
('Monitoring / wearables','NOT_SATURATED','No completed dedicated coverage category.'),
('Brazil-specific evidence','NOT_SATURATED','Only two bounded single-force studies are appraised.'),
('International transferability','PARTIALLY_SATURATED','Population/context transferability limits are repeatedly documented.'),
]
def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def write(n,r):
    with (OUT/n).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(r[0]) if r else ['Evidence_ID']);w.writeheader();w.writerows(r)
def claim_domain(cid):
    x=cid.lower()
    if any(k in x for k in ('phys','fitness','bodycomposition','load','armor')):return 'Physical / academy readiness'
    if any(k in x for k in ('nutrition','supplement','caffeine')):return 'Nutrition'
    if any(k in x for k in ('sleep','fatigue','cognition','firearm','vision')):return 'Sleep / fatigue / recovery'
    if any(k in x for k in ('tacmed','hemorrhage','tccc','tecc')):return 'Tactical medicine'
    if any(k in x for k in ('implement','barrier','acceptability')):return 'Implementation science'
    if any(k in x for k in ('msk','injury')):return 'Musculoskeletal injury'
    if any(k in x for k in ('cvd','medical')):return 'Medical / cardiovascular readiness'
    return 'Operational / occupational readiness'
def main():
    decisions=read(FT1/'PMC100_PROVISIONAL_DECISIONS.csv'); claims=read(FT1/'PMC100_CLAIM_CITATION_MATRIX.csv'); repl=read(FT1/'PMC100_REPLACEMENT_COMPARISON.csv'); high3=read(FT4/'HIGH3_PROVISIONAL_DECISIONS.csv'); high=read(FT5/'HIGH22_ACCESS_REMEDIATION_MASTER.csv'); med=read(FT7/'MEDIUM5_ACCESS_RECOVERY_MASTER.csv')
    assert len(decisions)==100 and len(claims)==71 and len(high)==22 and len(med)==5
    domain_rows=[]
    for domain,status,rationale in DOMAINS:
        domain_rows.append({'Domain':domain,'Saturation_Status':status,'Rationale':rationale,'PMC100_Claim_Mappings':str(sum(claim_domain(c['Claim_ID'])==domain for c in claims)),'Unresolved_HIGH_Exists':'YES' if status in {'BLOCKED_BY_ACCESS','BLOCKED_BY_UNRESOLVED_CONTRADICTORY_EVIDENCE'} else 'NO','Contradictory_Risk':'MATERIAL' if status=='BLOCKED_BY_UNRESOLVED_CONTRADICTORY_EVIDENCE' else ('MODERATE' if status=='BLOCKED_BY_ACCESS' else 'RESIDUAL'),'Access_Limitation':'MATERIAL' if status.startswith('BLOCKED') else ('MODERATE' if status in {'PARTIALLY_SATURATED','NOT_SATURATED'} else 'LOW'),'Human_Confirmation':'PENDING'})
    write('DOMAIN_SATURATION_ADJUDICATION.csv',domain_rows)
    group=defaultdict(list)
    for c in claims:group[c['Claim_ID']].append(c)
    domain_status={x[0]:x[1] for x in DOMAINS}; claim_rows=[]
    for cid,items in sorted(group.items()):
        d=claim_domain(cid); st=domain_status[d]; first=items[0]
        claim_rows.append({'Claim_ID':cid,'Manuscript':first['Manuscript_Layer'],'Section':'As mapped in PMC100 ledger','Claim_Wording':first['Claim_Current_Wording'],'Current_References':'Current reference map not re-adjudicated in FT8','Appraised_Support':str(len(items))+' provisional full-text mappings','Directness':'; '.join(sorted({x['Transferability'] for x in items})),'Certainty':'AI-provisional; human confirmation pending','Null_Evidence':'Preserved in source-level FT1 ledgers where reported','Contradictory_Evidence':'UNADJUDICATED_HIGH_RELEVANT' if st=='BLOCKED_BY_UNRESOLVED_CONTRADICTORY_EVIDENCE' else 'No material unadjudicated contradictory HIGH mapped','Unresolved_HIGH':'YES' if st.startswith('BLOCKED') else 'NO','Replacement_Candidate':'YES' if any(x['Evidence_ID'] in {r['Evidence_ID'] for r in repl} for x in items) else 'NO','Incremental_Value_of_More_Evidence':'MATERIAL' if st.startswith('BLOCKED') or st=='NOT_SATURATED' else 'MODERATE','Saturation_Status':st,'Rationale':'FT8 adjudication is evidence-layer only; does not create Claim-Ready or final scientific approval.'})
    # The three FT4 claims are explicitly preserved even if not present in the FT1 matrix.
    for h in high3:
        cid={'EV-1462':'INT-SLEEP-CAFFEINE-MITIGATION','EV-1463':'BRA-PMDF-CVD-SURVEILLANCE','EV-1466':'BRA-PM-PAIN-CONTEXT'}[h['Evidence_ID']]
        d={'EV-1462':'Sleep / fatigue / recovery','EV-1463':'Medical / cardiovascular readiness','EV-1466':'Musculoskeletal injury'}[h['Evidence_ID']]
        claim_rows.append({'Claim_ID':cid,'Manuscript':'International' if h['Evidence_ID']=='EV-1462' else 'Brazil','Section':'FT4 claim matrix','Claim_Wording':h['Claim_Role'],'Current_References':'Not re-adjudicated','Appraised_Support':'One FT4 AI-provisional full-text appraisal','Directness':h['Directness'],'Certainty':'AI-provisional; human confirmation pending','Null_Evidence':'See FT4 results ledger','Contradictory_Evidence':'No adjudicated contradictory evidence','Unresolved_HIGH':'YES' if h['Evidence_ID']=='EV-1462' else 'NO','Replacement_Candidate':'YES' if h['Evidence_ID']=='EV-1462' else 'NO','Incremental_Value_of_More_Evidence':'MODERATE','Saturation_Status':domain_status[d],'Rationale':'Bounded by FT4 appraisal; no final inclusion.'})
    write('CLAIM_SATURATION_ADJUDICATION.csv',claim_rows)
    candidates=[]
    for r in decisions:
        role={'PROVISIONAL_INCLUDE':'FINAL_REFERENCE_CANDIDATE','PROVISIONAL_REPLACE_CANDIDATE':'FINAL_REPLACEMENT_CANDIDATE','CONTEXT_ONLY':'CONTEXT_REFERENCE_CANDIDATE','DISCUSSION_ONLY':'DISCUSSION_REFERENCE_CANDIDATE'}.get(r['Provisional_Decision'],'UNRESOLVED_NOT_ELIGIBLE' if r['Provisional_Decision'] in {'FULL_TEXT_INSUFFICIENT','UNRESOLVED'} else 'DO_NOT_USE')
        candidates.append({'Evidence_ID':r['Evidence_ID'],'Candidate_Status':role,'Source':'PMC100 FT1','Human_Confirmation':r['HUMAN_CONFIRMATION'],'Claim_Ready':r['CLAIM_READY_PROVISIONAL'],'Boundary':r['Prohibited_Inference']})
    candidates += [
      {'Evidence_ID':'EV-1462','Candidate_Status':'FINAL_REPLACEMENT_CANDIDATE','Source':'FT4','Human_Confirmation':'PENDING','Claim_Ready':'NO','Boundary':'Bounded caffeine/sleep-loss mitigation only.'},
      {'Evidence_ID':'EV-1463','Candidate_Status':'CONTEXT_REFERENCE_CANDIDATE','Source':'FT4','Human_Confirmation':'PENDING','Claim_Ready':'NO','Boundary':'PMDF cross-sectional surveillance only.'},
      {'Evidence_ID':'EV-1466','Candidate_Status':'CONTEXT_REFERENCE_CANDIDATE','Source':'FT4','Human_Confirmation':'PENDING','Claim_Ready':'NO','Boundary':'Weak ROC context only; no prevention inference.'}]
    write('FINAL_REFERENCE_CANDIDATE_LEDGER.csv',candidates)
    replacements=[x for x in candidates if x['Candidate_Status']=='FINAL_REPLACEMENT_CANDIDATE'];write('FINAL_REPLACEMENT_CANDIDATE_LEDGER.csv',replacements)
    contrad=[
      {'Evidence_ID':'EV-0052','Affected_Domain':'Physical / academy readiness','Affected_Claim':'Psychological screening/physical-performance relationship','Likely_Challenge':'May challenge a simple psychological self-report screen as a performance-decrement surrogate.','Access_Status':'PAYWALLED_NO_LAWFUL_FULL_TEXT_FOUND','Implication_for_Certainty':'MATERIAL; do not make a definitive screening claim.','Manuscript_Limitation_Required':'Disclose unadjudicated contradictory HIGH evidence.'},
      {'Evidence_ID':'EV-0140','Affected_Domain':'Nutrition','Affected_Claim':'Short-term dietary-fat effects on physical performance','Likely_Challenge':'May challenge claims that short-term moderately high-fat intake materially changes performance.','Access_Status':'PAYWALLED_NO_LAWFUL_FULL_TEXT_FOUND','Implication_for_Certainty':'MATERIAL; retain outcome-specific and cautious wording.','Manuscript_Limitation_Required':'Disclose unadjudicated contradictory HIGH evidence.'},
      {'Evidence_ID':'EV-1066','Affected_Domain':'Physical / academy readiness','Affected_Claim':'BMI/body-composition as an operational-readiness proxy','Likely_Challenge':'May challenge BMI as a global predictor of military-relevant task performance.','Access_Status':'PAYWALLED_NO_LAWFUL_FULL_TEXT_FOUND','Implication_for_Certainty':'MATERIAL; avoid BMI-only readiness inference.','Manuscript_Limitation_Required':'Disclose unadjudicated contradictory HIGH evidence.'}]
    write('UNRESOLVED_CONTRADICTORY_LEDGER.csv',contrad)
    access=[{'Evidence_Class':'HIGH','Count':'22','Risk':'MATERIAL','Impact':'Five domains remain blocked or contradiction-blocked; no inaccessible study promoted.'},{'Evidence_Class':'Targeted MEDIUM','Count':'5','Risk':'MODERATE','Impact':'No selected MEDIUM was recovered; limits remain explicit.'},{'Evidence_Class':'PMC100 fail-closed','Count':'15','Risk':'MODERATE','Impact':'Insufficient bodies cannot support claims.'}]
    write('ACCESS_LIMITATION_IMPACT.csv',access)
    stopping=[{'Criterion':str(i),'Requirement':req,'Status':status,'Rationale':why} for i,(req,status,why) in enumerate([
      ('Targeted HIGH recovery exhausted','YES','FT5 completed; remaining routes are documented.'),('Targeted MEDIUM recovery exhausted','YES','FT7 completed for all five selected records.'),('Remaining expected incremental gain low','PARTIAL','Not low for blocked contradicted/access domains; these are explicitly excluded from saturation.'),('Claims supported or limitations representable','PARTIAL','Only bounded/provisional claims can proceed, with mandatory limitations.'),('Unresolved contradictions documented','YES','Three HIGH contradictory records have an explicit ledger.'),('No high-probability accessible gap remains','YES','FT5/FT7 did not yield appraisal-ready bodies.')],1)]
    write('REFERENCE_STOPPING_RULE_AUDIT.csv',stopping)
    limitations=[{'Requirement_ID':'LIM-'+str(i),'Required_Manuscript_Limitation':x} for i,x in enumerate(['State that evidence synthesis remains AI-provisional and requires named human review before final scientific claims.','Do not state that caffeine resolves sleep loss or transfers automatically to Brazilian police.','Do not infer causality from PMDF cardiovascular or Bahia pain cross-sectional studies.','Disclose the three inaccessible unadjudicated HIGH contradictory records and narrow affected physical/nutrition claims.','Avoid BMI-only readiness, universal dietary-fat, or psychological-self-report screening claims.','Describe access limitations: 22 HIGH, five targeted MEDIUM and 15 PMC100 bodies unavailable/insufficient.'],1)]
    write('MANUSCRIPT_LIMITATIONS_REQUIRED.csv',limitations)
    closure=[{'Area':'Evidence manifests and ledgers','Status':'READY','Rationale':'FT1/FT4/FT5/FT6/FT7 ledgers and manifests are versioned.'},{'Area':'Claims/reference candidates','Status':'PARTIAL','Rationale':'Candidates are AI-provisional; human confirmation and final reference selection remain pending.'},{'Area':'Saturation decision','Status':'REFERENCE_SATURATION_PARTIAL_PASS','Rationale':'Proceed only with narrowed claims and mandatory limitations; blocked domains cannot be represented as saturated.'},{'Area':'GitHub evidence layer','Status':'GITHUB_EVIDENCE_LAYER_PARTIAL','Rationale':'Provenance/versioning/tests are ready; scientific confirmation remains incomplete.'}]
    write('REFERENCE_SET_CLOSURE_READINESS.csv',closure)
    statuses=defaultdict(int)
    for x in domain_rows:statuses[x['Saturation_Status']]+=1
    roles=defaultdict(int)
    for x in candidates:roles[x['Candidate_Status']]+=1
    report=f'''# Batch 10.4B-FT8 — domain saturation adjudication\n\nAll 17 mandated domains and {len(claim_rows)} claim-level entries were adjudicated from existing versioned ledgers. No new search, full-text retrieval, appraisal, manuscript, Zotero or CEF change occurred.\n\n## Decision\n\n`REFERENCE_SATURATION_PARTIAL_PASS` for **manuscript revision preparation only**. This is not scientific approval, Claim-Ready release or final reference closure: human review remains pending for all candidates.\n\n- Domain statuses: {json.dumps(dict(statuses))}\n- Reference candidate statuses: {json.dumps(dict(roles))}\n- Unadjudicated contradictory HIGH records: 3\n- Access-limited records: 22 HIGH, 5 targeted MEDIUM, 15 PMC100 fail-closed\n\n`GO_BATCH10_4C_EVIDENCE_SATURATED_MANUSCRIPT` is limited to a v0.13 drafting pass that implements the required narrowing and limitations. It must not claim saturation in blocked domains or upgrade any AI-provisional candidate to final evidence.\n'''
    (OUT/'BATCH10_4B_FT8_REPORT.md').write_text(report,encoding='utf-8')
    files=sorted(p for p in OUT.iterdir() if p.name!='BATCH10_4B_FT8_MANIFEST.json')
    manifest={'batch':'BATCH10_4B_FT8','decision':'REFERENCE_SATURATION_PARTIAL_PASS','domains':17,'claims':len(claim_rows),'status_counts':dict(statuses),'cef_v1':'UNCHANGED','zotero':'UNCHANGED','manuscript':'UNCHANGED','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (OUT/'BATCH10_4B_FT8_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
