"""Build the limited, evidence-bound HR-006 replacement adjudication."""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4e'; AUDIT=ROOT/'batch10_4d'
DECISION={'HUMAN_DECISION':'KEEP_CURRENT','HUMAN_REVIEWER':'Matheus Florindo de Deus','HUMAN_REVIEW_DATE':'2026-10-06','HUMAN_RATIONALE':'After final comparative review of the current verified reference and EV-0426, the current reference was retained because it provides equal or superior claim alignment, directness, methodological suitability, and citation value for the manuscript.'}
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def write(p,fields,rows):
 with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)
def refresh():
 p=AUDIT/'BATCH10_4D_MANIFEST.json'; m=json.loads(p.read_text(encoding='utf-8')); q=AUDIT/'FINAL_HUMAN_REVIEW_QUEUE.csv'
 m['files'][q.name]=hashlib.sha256(q.read_bytes()).hexdigest();m.setdefault('human_adjudication_updates',{})['HR-006']={'evidence_id':'EV-0426','decision':'KEEP_CURRENT','reviewer':'Matheus Florindo de Deus','review_date':'2026-10-06','scope':'Retain EV-1471 and EV-1472 for their distinct, cited Brazilian shift-nutrition claims; do not promote EV-0426 as replacement or support.'}
 p.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
def main():
 dims=[
 ('claim alignment','EV-1471/EV-1472 support existing, specific Brazilian shift-nutrition claims in v0.13.','PARTIAL_SUPPORT for INT-NUTRITION-CAUTIOUS, absent as supporting text in v0.13.','CURRENT','v0.13 paragraphs 39-40 / 37-38; HR001 mapping'),
 ('population directness','22 and 34 Brazilian military police officers working shifts.','Active-duty military personnel across heterogeneous included studies.','CURRENT','Canonical master; FT1 extraction'),
 ('tactical/occupational relevance','Direct occupational police/shift context.','Military supplementation/recovery context, not police shift nutrition.','CURRENT','Canonical master; FT1 appraisal'),
 ('study design','Two small cross-sectional studies, bounded to associations.','Systematic review of randomized and quasi-experimental controlled trials.','NO AUTOMATIC WIN','Canonical master; FT1 appraisal'),
 ('sample adequacy','22 and 34 direct-population participants; explicitly limited in manuscript.','16 heterogeneous studies; pooled applicability constrained.','CURRENT','v0.13; FT1 extraction'),
 ('outcome alignment','Dietary intake, meal timing, vigilance and shift-condition outcomes match current wording.','Muscle performance and recovery after supplements; no meal timing/vigilance outcome.','CURRENT','v0.13; FT1 extraction'),
 ('methodological quality','Verified retained studies used only for their descriptive, noncausal roles.','AMSTAR 2 CRITICALLY_LOW_CONFIDENCE.','CURRENT','FINAL_REFERENCE_AUDIT; FT1 appraisal'),
 ('risk of bias','No integrity block recorded; limitations disclosed in wording.','Critically low confidence: two databases, English restriction, heterogeneity and limited search comprehensiveness.','CURRENT','FINAL_REFERENCE_AUDIT; FT1 risk-of-bias ledger'),
 ('statistical informativeness','Current cited effect estimates and schedule-pattern data answer their exact claims.','Findings inconsistent and mostly modest; inadequate practical evidence for field-performance guidance.','CURRENT','v0.13; FT1 extraction'),
 ('recency','2025 and 2026.','2024.','CURRENT','FINAL_REFERENCE_AUDIT; canonical master'),
 ('generalizability','Geographically bounded Brazilian studies; manuscript explicitly forbids national generalization.','Low-to-moderate transferability across heterogeneous military interventions.','CURRENT','v0.13; FT1 appraisal'),
 ('Brazil relevance','Direct Brazilian public-safety population.','Direct transfer to Brazilian public safety is prohibited.','CURRENT','Canonical master; FT1 prohibited inference'),
 ('international relevance','Current roles are retained as a bounded Brazilian adaptation case.','Military context could be contextual only, but not for an active v0.13 claim.','CURRENT','v0.13 / HR001 mapping; FT1 appraisal'),
 ('incremental value','Retains cited, claim-specific evidence without inflation.','No material value for existing wording; would create a new supplementation pathway.','CURRENT','HR001 mapping; FT1 extraction'),
 ('overlap/redundancy','References cover distinct intake-vigilance and chrononutrition claims.','Review-level overlap with primary studies; no claim-equivalent added value.','CURRENT','v0.13; PMC100 cohort-overlap ledger'),
 ('integrity','No integrity block in versioned QA.','INTEGRITY_CLEAR_AS_OF_2026-10-03, date-bounded.','TIE','FINAL_REFERENCE_AUDIT; FT1 integrity ledger'),
 ('citation fitness','Cited in both v0.13 versions (2 International and 2 Brazil citations each).','PARTIAL_SUPPORT, HUMAN_REVIEW_PENDING and no manuscript citation.','CURRENT','FINAL_REFERENCE_AUDIT; PMC100 claim matrix'),
 ('suitability for exact manuscript wording','Supports current association-only wording and explicit noncausal limits.','Would require a new, narrowed supplementation statement and cannot improve the existing claims.','CURRENT','v0.13; HR001 map; FT1 prohibited inference')]
 comparison=[{'Comparison_ID':'HR006-REPL-EV-0426','Dimension_Number':i,'Dimension':d,'Current_Reference_Set':'EV-1471 (Ref 3) + EV-1472 (Ref 4)','Current_Evidence':c,'EV0426_Evidence':e,'Finding_Favors':f,'Source':s,'Final_Classification':'KEEP_CURRENT'} for i,(d,c,e,f,s) in enumerate(dims,1)]
 write(OUT/'HR006_REPLACEMENT_COMPARISON.csv',list(comparison[0]),comparison)
 impact=[
 {'Claim_ID':'BR-NUTRITION-VIGILANCE','Manuscript':'Both','Current_Wording':'Small, cross-sectional Brazilian police study: intake patterns and selected vigilance metrics varied under specific shift conditions; no dietary causality.','Current_Citation':'EV-1471 / Ref 3','EV0426_Relevance':'Does not directly assess police vigilance, caloric intake or shift condition.','Support':'NO_DIRECT_SUPPORT','Effect_If_Replaced':'Weakens directness and removes the only cited claim-specific study.','Effect_If_Both':'Adds a non-equivalent supplementation review without a sentence-level role.','Wording_Change_Required':'NO','Decision':'KEEP_CURRENT'},
 {'Claim_ID':'BR-CHRONONUTRITION-SHIFT','Manuscript':'Both','Current_Wording':'Shift schedule was associated with dietary intake, composition and eating-window patterns in 34 Brazilian military police officers; no prescription or performance effect.','Current_Citation':'EV-1472 / Ref 4','EV0426_Relevance':'Does not assess chrononutrition or meal timing.','Support':'NO_DIRECT_SUPPORT','Effect_If_Replaced':'Eliminates the direct chrononutrition context.','Effect_If_Both':'Creates reference inflation without improving current wording.','Wording_Change_Required':'NO','Decision':'KEEP_CURRENT'},
 {'Claim_ID':'INT-NUTRITION-CAUTIOUS','Manuscript':'Both','Current_Wording':'NOT PRESENT AS A SUPPORTING CLAIM IN V0.13.','Current_Citation':'No assigned v0.13 citation','EV0426_Relevance':'PARTIAL_SUPPORT: heterogeneous, mostly modest findings and inadequate practical field-performance guidance.','Support':'PARTIAL_ONLY','Effect_If_Replaced':'Would require a new narrowed sentence and separate approval.','Effect_If_Both':'Still requires a new claim/citation path; not authorized.','Wording_Change_Required':'YES IF EVER CITED; NOT AUTHORIZED HERE','Decision':'KEEP_CURRENT'}]
 write(OUT/'HR006_CLAIM_IMPACT.csv',list(impact[0]),impact)
 record={'Review_ID':'HR-006','Evidence_ID':'EV-0426','Replacement_Relationship':'DETERMINISTIC: EV-1471; EV-1472','Final_Classification':'KEEP_CURRENT',**DECISION,'Current_References_Retained':'EV-1471 (Ref 3); EV-1472 (Ref 4)','EV0426_Use':'Not promoted as support or replacement; no manuscript change.','Final_Reference_Freeze':'NO'}
 write(OUT/'HR006_HUMAN_DECISION_RECORD.csv',list(record),[record])
 qp=AUDIT/'FINAL_HUMAN_REVIEW_QUEUE.csv'; q=read(qp)
 for r in q:
  if r['Review_ID']=='HR-006':r.update(DECISION)
 target=[r for r in q if r['Review_ID']=='HR-006']
 if len(target)!=1 or target[0]['HUMAN_DECISION']!='KEEP_CURRENT':raise RuntimeError('HR-006 not uniquely updated')
 write(qp,list(q[0]),q);refresh()
 (OUT/'HR006_REPORT.md').write_text('''# HR-006 — EV-0426 final reference decision

The deterministic replacement relationship is EV-0426 against EV-1471 (reference 3) and EV-1472 (reference 4). The 18-dimension comparison confirms `KEEP_CURRENT`: the retained studies provide the exact, bounded Brazilian police claims on intake/vigilance and chrononutrition/shift schedules. EV-0426 is a full-text systematic review, but has AMSTAR 2 `CRITICALLY_LOW_CONFIDENCE`, low-to-moderate transferability, and only partial support for an absent supplement claim. Its 16 included studies had inconsistent, mostly modest findings and inadequate practical evidence for field-performance guidance.

Matheus Florindo de Deus recorded the conditionally authorized `KEEP_CURRENT` decision on 2026-10-06. EV-0426 was not promoted to support or a replacement. No manuscript, reference freeze, CEF-v1, Zotero, or Claim-Ready change occurred. Red Team found no recency, novelty, journal/design-prestige, claim/population/outcome mismatch, or reference-inflation basis for substitution.

Gate: `HR006_ADJUDICATION_COMPLETE`; next authorized item: `GO_HR007_HUMAN_ADJUDICATION`.
''',encoding='utf-8')
if __name__=='__main__':main()
