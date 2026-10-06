"""Build the constrained HR-007 adjudication for EV-0521."""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]; O=R/'batch10_4e'; A=R/'batch10_4d'
D={'HUMAN_DECISION':'KEEP_CURRENT','HUMAN_REVIEWER':'Matheus Florindo de Deus','HUMAN_REVIEW_DATE':'2026-10-06','HUMAN_RATIONALE':'After final comparative review of the current verified reference architecture and EV-0521, the current reference was retained because it provides equal or superior claim alignment, directness, methodological suitability, and citation value, without a material incremental benefit from replacement.'}
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def write(p,f,x):
 with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=f);w.writeheader();w.writerows(x)
def main():
 data=[
 ('claim alignment','EV-1471/1472 support existing shift-nutrition/vigilance and chrononutrition claims.','DIRECT_SUPPORT only for INT-FIREFIGHTER-SUPPLEMENT-SPECIFIC, absent from v0.13.','CURRENT','v0.13 paragraphs 39-40 / 37-38; HR001 map'),
 ('population directness','22 and 34 Brazilian military police officers working shifts.','30 male career firefighters.','CURRENT','Canonical master; PMC100 extraction'),
 ('tactical/occupational relevance','Direct policing and shift-work context.','Direct firefighter task context, but supplementation-specific.','CURRENT','v0.13; PMC100 extraction'),
 ('study design','Cross-sectional evidence used only for associations.','Randomized parallel-group double-blind trial.','NO AUTOMATIC WIN','Canonical master; FT1 appraisal'),
 ('sample adequacy','Small direct-population samples, limitations explicitly disclosed.','30 male firefighters.','CURRENT','v0.13; PMC100 extraction'),
 ('outcome alignment','Intake, meal timing and vigilance match current wording.','Selected fire-ground task times after creatine/protein/carbohydrate; not shift nutrition or vigilance.','CURRENT','v0.13; PMC100 extraction'),
 ('methodological quality','Verified studies retained solely for bounded descriptive roles.','RoB 2 SOME_CONCERNS.','CURRENT','FINAL_REFERENCE_AUDIT; FT1 appraisal'),
 ('risk of bias','No integrity block in versioned QA; noncausal limits are explicit.','Small all-male sample, no inert control, and unresolved randomization/outcome-assessment concerns.','CURRENT','FINAL_REFERENCE_AUDIT; FT1 risk-of-bias ledger'),
 ('statistical informativeness','Exact cited associations and schedule-pattern results answer current claims.','Creatine group improved rescue (1.78 s, 95% CI .61-2.95) and forcible entry (2.66 s, .68-4.65), with no interaction for other tasks or total time.','CURRENT','PMC100 extraction'),
 ('recency','2025 and 2026.','2023.','CURRENT','FINAL_REFERENCE_AUDIT; canonical master'),
 ('generalizability','Bounded Brazilian studies, explicitly not national norms.','Moderate transferability; no female-firefighter or Brazilian-agency generalization.','CURRENT','v0.13; FT1 appraisal'),
 ('Brazil relevance','Direct Brazilian public-safety populations.','No Brazilian public-safety inference permitted.','CURRENT','Canonical master; FT1 prohibited inference'),
 ('international relevance','Existing references are used as bounded adaptation evidence.','Potentially relevant firefighter trial but no active manuscript claim.','CURRENT','v0.13/HR001 mapping; FT1 appraisal'),
 ('incremental value','Retains exact claims with no bibliography inflation.','No material value for active wording; would require a new, highly bounded supplement claim.','CURRENT','HR001 mapping; PMC100 extraction'),
 ('overlap/redundancy','Records cover distinct intake-vigilance and chrononutrition claims.','No cohort overlap, but adding it creates a separate uncited claim pathway.','CURRENT','v0.13; PMC100 cohort-overlap ledger'),
 ('integrity','No integrity block in versioned QA.','INTEGRITY_CLEAR_AS_OF_2026-10-03, date-bounded.','TIE','FINAL_REFERENCE_AUDIT; FT1 integrity ledger'),
 ('citation fitness','Both current references are cited twice in International and Brazil.','DIRECT_SUPPORT but HUMAN_REVIEW_PENDING and not cited in v0.13.','CURRENT','FINAL_REFERENCE_AUDIT; PMC100 claim matrix'),
 ('suitability for exact manuscript wording','Matches association-only, shift-specific wording.','Would require a new narrow firefighter/creatine sentence and risks overclaim if generalized.','CURRENT','v0.13; HR001 map; FT1 prohibited inference')]
 c=[{'Comparison_ID':'HR007-REPL-EV-0521','Dimension_Number':i,'Dimension':d,'Current_Reference_Set':'EV-1471 (Ref 3) + EV-1472 (Ref 4)','Current_Evidence':x,'EV0521_Evidence':y,'Finding_Favors':z,'Source':s,'Final_Classification':'KEEP_CURRENT'} for i,(d,x,y,z,s) in enumerate(data,1)]
 write(O/'HR007_REPLACEMENT_COMPARISON.csv',list(c[0]),c)
 impacts=[
 {'Claim_ID':'BR-NUTRITION-VIGILANCE','Manuscript':'Both','Section':'Nutrition and Schedule Load / Nutrição e jornadas','Current_Wording':'Intake patterns and selected vigilance metrics varied under specific shift conditions; no dietary causality.','Current_Citation':'EV-1471 / Ref 3','Current_Support':'DIRECT_FOR_EXISTING_BOUNDED_CLAIM','EV0521_Support':'NO_DIRECT_SUPPORT','Directness_Difference':'CURRENT_HIGHER','Certainty_Difference':'NO_REPLACEMENT_GAIN','Replacement_Requires_Narrowing':'YES','Replacement_Creates_Overclaim':'YES','Both_Complementary_Value':'NO_ACTIVE_SENTENCE_ROLE','Decision':'KEEP_CURRENT'},
 {'Claim_ID':'BR-CHRONONUTRITION-SHIFT','Manuscript':'Both','Section':'Nutrition and Schedule Load / Nutrição e jornadas','Current_Wording':'Shift schedule was associated with dietary intake, composition and eating-window patterns; no prescription or performance effect.','Current_Citation':'EV-1472 / Ref 4','Current_Support':'DIRECT_FOR_EXISTING_BOUNDED_CLAIM','EV0521_Support':'NO_DIRECT_SUPPORT','Directness_Difference':'CURRENT_HIGHER','Certainty_Difference':'NO_REPLACEMENT_GAIN','Replacement_Requires_Narrowing':'YES','Replacement_Creates_Overclaim':'YES','Both_Complementary_Value':'NO_ACTIVE_SENTENCE_ROLE','Decision':'KEEP_CURRENT'},
 {'Claim_ID':'INT-FIREFIGHTER-SUPPLEMENT-SPECIFIC','Manuscript':'Both','Section':'NOT_PRESENT_AS_SUPPORTING_SECTION','Current_Wording':'NOT PRESENT AS A SUPPORTING CLAIM IN V0.13.','Current_Citation':'No assigned v0.13 citation','Current_Support':'NOT_APPLICABLE','EV0521_Support':'DIRECT_SUPPORT_WITH_BOUNDARY','Directness_Difference':'CANDIDATE_ONLY_FOR_ABSENT_CLAIM','Certainty_Difference':'RoB2_SOME_CONCERNS','Replacement_Requires_Narrowing':'YES','Replacement_Creates_Overclaim':'YES_IF_GENERALIZED','Both_Complementary_Value':'NOT_UNTIL_HUMAN_APPROVED_SENTENCE','Decision':'KEEP_CURRENT'}]
 write(O/'HR007_CLAIM_IMPACT.csv',list(impacts[0]),impacts)
 rec={'Review_ID':'HR-007','Evidence_ID':'EV-0521','Replacement_Relationship':'DETERMINISTIC: EV-1471; EV-1472','Final_Classification':'KEEP_CURRENT',**D,'Current_References_Retained':'EV-1471 (Ref 3); EV-1472 (Ref 4)','EV0521_Use':'Not promoted as support or replacement; no manuscript change.','Final_Reference_Freeze':'NO'}
 write(O/'HR007_HUMAN_DECISION_RECORD.csv',list(rec),[rec])
 qpath=A/'FINAL_HUMAN_REVIEW_QUEUE.csv';q=read(qpath)
 for r in q:
  if r['Review_ID']=='HR-007':r.update(D)
 if len([r for r in q if r['Review_ID']=='HR-007' and r['HUMAN_DECISION']=='KEEP_CURRENT'])!=1:raise RuntimeError('HR-007 update failed')
 write(qpath,list(q[0]),q)
 mpath=A/'BATCH10_4D_MANIFEST.json';m=json.loads(mpath.read_text(encoding='utf-8'));m['files'][qpath.name]=hashlib.sha256(qpath.read_bytes()).hexdigest();m.setdefault('human_adjudication_updates',{})['HR-007']={'evidence_id':'EV-0521','decision':'KEEP_CURRENT','reviewer':'Matheus Florindo de Deus','review_date':'2026-10-06','scope':'Retain EV-1471 and EV-1472 for their distinct cited Brazilian shift-nutrition claims; do not promote EV-0521.'};mpath.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 (O/'HR007_REPORT.md').write_text('''# HR-007 — EV-0521 final reference decision

The deterministic relationship is EV-0521 against EV-1471 (reference 3) and EV-1472 (reference 4). The documented 18-dimension and claim-level comparison supports `KEEP_CURRENT`. The retained references serve the exact v0.13 claims on Brazilian police shift nutrition, vigilance and chrononutrition. EV-0521 is a small male-firefighter trial with `RoB 2 = SOME_CONCERNS`; its selected creatine-associated task-time findings do not assess the current police outcomes, and it cannot support generalized supplementation claims.

Matheus Florindo de Deus recorded the conditionally authorized `KEEP_CURRENT` decision on 2026-10-06. EV-0521 is not promoted to support or replacement. Manuscripts, CEF-v1, Zotero, Claim-Ready and final-reference freeze remain unchanged. Red Team found no valid recency, novelty, prestige or design basis for a claim-mismatched substitution.

Gate: `HR007_ADJUDICATION_COMPLETE`; next authorized item: `GO_HR008_HUMAN_ADJUDICATION`.
''',encoding='utf-8')
if __name__=='__main__':main()
