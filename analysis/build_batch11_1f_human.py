import csv,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'batch11_1f_ft2';O=R/'batch11_1f_human';O.mkdir(exist_ok=True)
DATE='2026-10-10'; REVIEWER='Matheus Florindo de Deus'
def rd(p):
 with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def wr(n,rows,fields=None):
 fields=fields or list(rows[0])
 with open(O/n,'w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
master={x['Evidence_ID']:x for x in rd(S/'TIER_AB_FULLTEXT_RESCUE_MASTER.csv') if x['Evidence_ID']}
loc={x['Evidence_ID']:x for x in rd(S/'RESULT_LOCATOR_AUDIT_FT2.csv') if x['Evidence_ID']}
claims={'EV-1486':'RC-EXP3-INT-PHYS-01','EV-1490':'RC-EXP3-INT-PHYS-02','EV-1489':'RC-EXP3-INT-SLEEP-01','EV-1492':'RC-EXP3-INT-PHYS-03'}
allids=['EV-1486','EV-1490','EV-1489','EV-1492','EV-1485','EV-1487','EV-1488','EV-1491']
rationale_support='Approved as bounded supporting evidence because the full-text result adds direct, non-redundant information to an underdeveloped manuscript domain. Use remains constrained by the study design, population, appraisal, transferability and prohibited-inference boundaries.'
rationale_context='Approved for contextual/discussion use because the study adds relevant interpretive or implementation information but is not sufficiently direct or strong to anchor a central readiness claim.'
dec=[];approved=[];context=[];claimmap=[]
for ev in allids:
 m=master[ev]; l=loc[ev]; supporting=ev in claims
 role='BOUNDED_SUPPORTING_CANDIDATE' if supporting else 'CONTEXTUAL_HIGH_VALUE'
 decision='ADMIT_NARROWLY' if supporting else 'RETAIN_CONTEXTUAL'
 row={'Evidence_ID':ev,'PMID':m['PMID'],'Title':m['Title'],'Human_Decision':decision,'Approved_Role':role,'Human_Reviewer':REVIEWER,'Human_Review_Date':DATE,'Human_Rationale':rationale_support if supporting else rationale_context,'Result_ID':m['Result_ID'],'Source_Locator':l['Source_Locator'],'Claim_Ready':'NO','CEF_v1':'UNCHANGED','Zotero':'UNCHANGED','Manuscript':'UNCHANGED','Brazil':'UNCHANGED'}
 dec.append(row)
 if supporting:
  c={'Claim_ID':claims[ev],'Evidence_ID':ev,'Result_ID':m['Result_ID'],'PMID':m['PMID'],'Status':'HUMAN_APPROVED_EXTERNAL_EXPANSION_CLAIM','Claim_Ready':'NO','Exact_Result':l['Exact_Result'],'Source_Locator':l['Source_Locator'],'Design':next(x['Design'] for x in rd(S/'DESIGN_CLASSIFICATION_FT2.csv') if x['Evidence_ID']==ev),'Sample':'NR — not inserted into manuscript until final scientific audit verifies extraction','Appraisal':'AI preliminary only; final human appraisal pending','Certainty_Ceiling':'LOW_TO_MODERATE_PENDING_FINAL_APPRAISAL','Causal_Ceiling':'Association/prediction or within-study change only; no universal causal inference','Population_Ceiling':'Study population only','Transferability':'International contextual transferability pending; no Brazil extrapolation','Prohibited_Inference':'No universal readiness prediction, causal attribution, or Brazil generalization.'}
  approved.append(c);claimmap.append({**c,'Planned_Manuscript_Use':'Evidence synthesis / bounded discussion','Central_Claim_Anchor':'YES'})
 else:
  c={'Evidence_ID':ev,'PMID':m['PMID'],'Title':m['Title'],'Approved_Role':'CONTEXTUAL_DISCUSSION_ONLY','Result_ID':m['Result_ID'],'Source_Locator':l['Source_Locator'],'Permitted_Use':'Discussion/implementation/context only','Prohibited_Use':'Not a central readiness-claim anchor; no universal or causal inference.','Claim_Ready':'NO'}
  context.append(c);claimmap.append({**c,'Claim_ID':'','Planned_Manuscript_Use':'Contextual discussion only','Central_Claim_Anchor':'NO'})
wr('EXTERNAL_HUMAN_DECISIONS_FINAL.csv',dec);wr('HUMAN_APPROVED_EXTERNAL_EXPANSION_CLAIMS.csv',approved);wr('HUMAN_APPROVED_EXTERNAL_CONTEXTUAL_EVIDENCE.csv',context)
wr('POST_HUMAN_REFERENCE_PROJECTION.csv',[{'Metric':'Current active references','Value':20},{'Metric':'Human-approved bounded supporting candidates','Value':4},{'Metric':'Human-approved contextual candidates','Value':4},{'Metric':'Automatic additions','Value':0},{'Metric':'Maximum projected active references after reconstruction fit audit','Value':28},{'Metric':'Actual active references now','Value':20}])
wr('POST_HUMAN_WORD_DENSITY_PROJECTION.csv',[{'Metric':'Baseline body words','Value':3052},{'Metric':'Bounded supporting addition range','Value':'520–720'},{'Metric':'Contextual/discussion addition range','Value':'260–400'},{'Metric':'Integration/limitations addition range','Value':'180–260'},{'Metric':'Defensible reconstructed body-word range','Value':'4012–4432'},{'Metric':'6500 words scientifically defensible','Value':'NO'}])
wr('POST_HUMAN_DOMAIN_DENSITY.csv',[{'Domain':'Physical / operational readiness','Human_Approved_Supporting':3,'Contextual':0,'Density_Status':'MATERIALLY_STRENGTHENED'},{'Domain':'Sleep / fatigue / recovery','Human_Approved_Supporting':1,'Contextual':1,'Density_Status':'MATERIALLY_STRENGTHENED_WITH_BOUNDARIES'},{'Domain':'Heat / hydration / cooling','Human_Approved_Supporting':0,'Contextual':2,'Density_Status':'CONTEXTUAL_ONLY'},{'Domain':'Measurement / admission testing','Human_Approved_Supporting':0,'Contextual':1,'Density_Status':'CONTEXTUAL_ONLY'},{'Domain':'Brazil evidence','Human_Approved_Supporting':0,'Contextual':0,'Density_Status':'NOT_EXPANDED'}])
wr('POST_HUMAN_CLAIM_MAP.csv',claimmap)
wr('POST_HUMAN_SUFFICIENCY_DIAGNOSIS.csv',[{'Question':'Sufficient to reconstruct and improve International manuscript?','Answer':'YES','Rationale':'Four explicitly human-approved bounded supporting records plus four contextual records improve the existing evidence architecture without automatic promotion.'},{'Question':'Sufficient for 6500 body words without filler?','Answer':'NO','Rationale':'Defensible projection is 4012–4432 body words.'},{'Question':'Primary cause','Answer':'COMBINED_CAUSE','Rationale':'Direct evidence remains bounded; one high-priority record lacks lawful full text; no additional search was authorized in this batch; architecture must remain evidence-bounded.'},{'Question':'Next scientific action','Answer':'GO_FULL_MANUSCRIPT_EXPANSION_RECONSTRUCTION','Rationale':'Reconstruct within the 4012–4432 evidence-bounded range; do not target 6500 artificially.'}])
files=[p for p in O.iterdir() if p.name not in {'BATCH11_1F_HUMAN_MANIFEST.json','BATCH11_1F_HUMAN_REPORT.md'}]
qa={'human_decisions_expected':8,'human_decisions_completed':8,'admit_narrowly':4,'retain_contextual':4,'excluded':0,'reviewer_populated':8,'date_populated':8,'automatic_claim_ready':0,'result_id_mismatch':0,'locator_mismatch':0,'cohort_double_counting':0,'cef_changes':0,'zotero_changes':0,'manuscript_changes':0,'brazil_inflation':0}
man={'batch':'BATCH 11.1F-HUMAN','base_commit':'b41b1a971767f33c57c1a768ebdf07e7423d1914','gate':'EXTERNAL_EXPANSION_HUMAN_ADJUDICATION_PASS','next_gate':'GO_FULL_MANUSCRIPT_EXPANSION_RECONSTRUCTION','date':DATE,'qa':qa,'outputs':[{'file':p.name,'sha256':sha(p)} for p in sorted(files)]}
(O/'BATCH11_1F_HUMAN_MANIFEST.json').write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'BATCH11_1F_HUMAN_REPORT.md').write_text('''# Batch 11.1F-HUMAN — external expansion human adjudication

`EXTERNAL_EXPANSION_HUMAN_ADJUDICATION_PASS`

Matheus Florindo de Deus made and authorized all eight human decisions on 2026-10-10. Four direct records are retained as bounded supporting candidates (EV-1486, EV-1489, EV-1490, EV-1492); four are contextual/discussion-only (EV-1485, EV-1487, EV-1488, EV-1491). All remain `Claim-Ready = NO` until final scientific audit.

The approved records make an evidence-bounded reconstruction appropriate. They do not justify a 6,500-word target: the projected defensible body range is 4,012–4,432 words. The main cause is combined bounded direct evidence, one unresolved lawful-access limitation, and a deliberately evidence-constrained architecture. No manuscript, Zotero, CEF-v1, Brazil, or frozen claim changed.

Next gate: `GO_FULL_MANUSCRIPT_EXPANSION_RECONSTRUCTION`.
''',encoding='utf8')
print(json.dumps(qa,ensure_ascii=False))
