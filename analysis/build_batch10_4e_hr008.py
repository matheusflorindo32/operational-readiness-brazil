"""Produce the evidence-bounded HR-008 replacement adjudication."""
from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'batch10_4e';A=R/'batch10_4d'
D={'HUMAN_DECISION':'KEEP_CURRENT','HUMAN_REVIEWER':'Matheus Florindo de Deus','HUMAN_REVIEW_DATE':'2026-10-06','HUMAN_RATIONALE':'After final comparative review of the current verified reference architecture and EV-0667, the current reference was retained because it provides equal or superior claim alignment, directness, methodological suitability, and citation value without a material incremental benefit from replacement.'}
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def write(p,f,x):
 with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=f);w.writeheader();w.writerows(x)
def main():
 pairs=[
 ('claim alignment','EV-1481/1480 support active academy-fitness and cadet use-of-force claims.','DIRECT_SUPPORT only for INT-PHYS-MEASUREMENT, absent in v0.13.','CURRENT','v0.13 / HR001 mapping'),
 ('population directness','219 male PMTO recruits and 34 Brazilian police cadets.','34 Slovenian infantry members.','CURRENT','Canonical master; FT1 appraisal'),
 ('tactical/occupational relevance','Direct Brazilian police academy and cadet training contexts.','Military cardiorespiratory-test context.','CURRENT','Canonical master; FT1 appraisal'),
 ('study design','Longitudinal pre-post academy observation plus quasi-experimental cadet study.','Within-subject test-retest and criterion-validity study.','NO AUTOMATIC WIN','Canonical master; FT1 appraisal'),
 ('sample adequacy','219 recruits for academy study; 34 cadets for martial-arts study, with bounded claims.','34 infantry participants.','CURRENT','Canonical master; FT1 appraisal'),
 ('outcome alignment','Academy physical-fitness change and simulated use-of-force outcome match v0.13.','30-15 IFT reliability/validity against treadmill and 2-mile run; no academy change or use-of-force outcome.','CURRENT','v0.13; FT1 claim matrix'),
 ('methodological quality','Verified references confined to their respective claims.','COSMIN: SOME_CONCERNS.','CURRENT','FINAL_REFERENCE_AUDIT; FT1 appraisal'),
 ('risk of bias','No integrity block in versioned QA; claims remain bounded.','n=34, one infantry sample and prediction/criterion boundaries.','CURRENT','FINAL_REFERENCE_AUDIT; FT1 risk ledger'),
 ('statistical informativeness','Current evidence answers its actual claims.','ICCs .971/.960/.975 and correlations .695-.930 for a different measurement claim.','CURRENT','FT1 extraction'),
 ('recency','2022 and 2026.','2022.','TIE','Canonical master'),
 ('generalizability','Bounded Brazilian police populations; no universalization.','Moderate transferability only from one Slovenian infantry cohort.','CURRENT','v0.13; FT1 appraisal'),
 ('Brazil relevance','Direct Brazilian police relevance.','Brazilian-policing validation prohibited.','CURRENT','Canonical master; FT1 prohibited inference'),
 ('international relevance','Brazil evidence is retained as bounded adaptation.','Potential International measurement context but no active v0.13 claim.','CURRENT','v0.13 / HR001 map'),
 ('incremental value','Preserves active cited claims without inflation.','No incremental value unless a future human-approved 30-15 IFT sentence is added.','CURRENT','HR001 mapping'),
 ('overlap/redundancy','Current references have distinct academy and cadet roles.','No cohort overlap, but creates an uncited measurement pathway.','CURRENT','PMC100 overlap ledger; HR001'),
 ('integrity','No integrity block recorded.','INTEGRITY_CLEAR_AS_OF_2026-10-03, date-bounded.','TIE','FINAL_REFERENCE_AUDIT; FT1 integrity ledger'),
 ('citation fitness','Current references are cited 2/2 and 3/2 times in International/Brazil.','DIRECT_SUPPORT but HUMAN_REVIEW_PENDING and uncited.','CURRENT','FINAL_REFERENCE_AUDIT; PMC100 claim matrix'),
 ('suitability for exact manuscript wording','Matches existing bounded academy/cadet wording.','Requires new 30-15 IFT wording and cannot establish Brazilian policing or combat readiness.','CURRENT','v0.13; FT1 prohibited inference')]
 c=[{'Comparison_ID':'HR008-REPL-EV-0667','Dimension_Number':i,'Dimension':d,'Current_Reference_Set':'EV-1481 (Ref 12) + EV-1480 (Ref 13)','Current_Evidence':x,'EV0667_Evidence':y,'Finding_Favors':z,'Source':s,'Final_Classification':'KEEP_CURRENT'} for i,(d,x,y,z,s) in enumerate(pairs,1)]
 write(O/'HR008_REPLACEMENT_COMPARISON.csv',list(c[0]),c)
 rows=[
 {'Claim_ID':'BR-ACADEMY-FITNESS','Manuscript':'Both','Section':'Physical and Academy Readiness / Aptidão e academia','Current_Wording':'Physical capacity changed during Brazilian military police academy training; causal components are not isolated.','Current_Citation':'EV-1481 / Ref 12','Current_Support':'DIRECT_FOR_EXISTING_CLAIM','EV0667_Support':'NO_DIRECT_SUPPORT','Directness_Difference':'CURRENT_HIGHER','Certainty_Difference':'NO_REPLACEMENT_GAIN','Population_Difference':'Brazilian police recruits versus Slovenian infantry','Outcome_Difference':'Academy fitness change versus test measurement','Replacement_Requires_Narrowing':'YES','Replacement_Creates_Overclaim':'YES','Both_Complementary':'NO_ACTIVE_SENTENCE_ROLE','Decision':'KEEP_CURRENT'},
 {'Claim_ID':'BR-CADET-USE-OF-FORCE','Manuscript':'Both','Section':'Physical and Academy Readiness / Aptidão e academia','Current_Wording':'Supplemental martial-arts training was associated with simulated use-of-force performance in Brazilian cadets.','Current_Citation':'EV-1480 / Ref 13','Current_Support':'DIRECT_FOR_EXISTING_CLAIM','EV0667_Support':'NO_DIRECT_SUPPORT','Directness_Difference':'CURRENT_HIGHER','Certainty_Difference':'NO_REPLACEMENT_GAIN','Population_Difference':'Brazilian cadets versus Slovenian infantry','Outcome_Difference':'Simulated use of force versus cardiorespiratory test validity','Replacement_Requires_Narrowing':'YES','Replacement_Creates_Overclaim':'YES','Both_Complementary':'NO_ACTIVE_SENTENCE_ROLE','Decision':'KEEP_CURRENT'},
 {'Claim_ID':'INT-PHYS-MEASUREMENT','Manuscript':'International','Section':'NOT_PRESENT_AS_SUPPORTING_SECTION','Current_Wording':'NOT PRESENT AS A SUPPORTING CLAIM IN V0.13.','Current_Citation':'No assigned v0.13 citation','Current_Support':'NOT_APPLICABLE','EV0667_Support':'DIRECT_SUPPORT_WITH_BOUNDARY','Directness_Difference':'CANDIDATE_ONLY_FOR_ABSENT_CLAIM','Certainty_Difference':'COSMIN_SOME_CONCERNS','Population_Difference':'One Slovenian infantry cohort','Outcome_Difference':'30-15 IFT reproducibility/criterion validity','Replacement_Requires_Narrowing':'YES','Replacement_Creates_Overclaim':'YES_IF_GENERALIZED','Both_Complementary':'NOT_UNTIL_HUMAN_APPROVED_SENTENCE','Decision':'KEEP_CURRENT'}]
 write(O/'HR008_CLAIM_IMPACT.csv',list(rows[0]),rows)
 rec={'Review_ID':'HR-008','Evidence_ID':'EV-0667','Replacement_Relationship':'DETERMINISTIC: EV-1481; EV-1480','Final_Classification':'KEEP_CURRENT',**D,'Current_References_Retained':'EV-1481 (Ref 12); EV-1480 (Ref 13)','EV0667_Use':'Not promoted as support or replacement; no manuscript change.','Final_Reference_Freeze':'NO'};write(O/'HR008_HUMAN_DECISION_RECORD.csv',list(rec),[rec])
 qp=A/'FINAL_HUMAN_REVIEW_QUEUE.csv';q=read(qp)
 for r in q:
  if r['Review_ID']=='HR-008':r.update(D)
 if len([r for r in q if r['Review_ID']=='HR-008' and r['HUMAN_DECISION']=='KEEP_CURRENT'])!=1:raise RuntimeError('HR-008 update failed')
 write(qp,list(q[0]),q);mp=A/'BATCH10_4D_MANIFEST.json';m=json.loads(mp.read_text(encoding='utf-8'));m['files'][qp.name]=hashlib.sha256(qp.read_bytes()).hexdigest();m.setdefault('human_adjudication_updates',{})['HR-008']={'evidence_id':'EV-0667','decision':'KEEP_CURRENT','reviewer':'Matheus Florindo de Deus','review_date':'2026-10-06','scope':'Retain EV-1481 and EV-1480 for their cited Brazilian academy/cadet claims; do not promote EV-0667.'};mp.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 (O/'HR008_REPORT.md').write_text('''# HR-008 — EV-0667 final reference decision

EV-0667 has a deterministic relationship to EV-1481 (reference 12) and EV-1480 (reference 13). The 18-dimension and claim-level comparison confirms `KEEP_CURRENT`: the retained references support active, bounded Brazilian academy-fitness and cadet use-of-force claims. EV-0667 is a 34-participant Slovenian-infantry 30-15 IFT measurement study, with COSMIN `SOME_CONCERNS`; it supports only an absent, narrowly measurement-specific claim and cannot validate Brazilian policing, combat readiness or outcome prediction.

Matheus Florindo de Deus recorded the conditionally authorized `KEEP_CURRENT` decision on 2026-10-06. No manuscript, Zotero, CEF-v1, Claim-Ready or final-reference-freeze action occurred. Red Team found no valid novelty, prestige or design rationale for substitution.

Gate: `HR008_ADJUDICATION_COMPLETE`; next authorized item: `GO_HR009_HUMAN_ADJUDICATION`.
''',encoding='utf-8')
if __name__=='__main__':main()
