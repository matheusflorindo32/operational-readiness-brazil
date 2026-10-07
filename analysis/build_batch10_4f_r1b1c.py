"""Batch 10.4F-R1B1C: result-level extraction from previously recovered lawful sources.
No manuscript, Zotero, CEF-v1, or sentence-adjudication mutation occurs here.
"""
import csv, hashlib, json
from collections import defaultdict
from pathlib import Path

R = Path(__file__).resolve().parents[1]
O = R / 'batch10_4f_r1b1c'


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as h:
        return list(csv.DictReader(h))


def write(path, fields, rows):
    path.parent.mkdir(exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as h:
        w = csv.DictWriter(h, fieldnames=fields, extrasaction='ignore')
        w.writeheader(); w.writerows(rows)


def main():
    inv = read(R/'batch10_4f_r1b1'/'FINAL_16_REFERENCE_SOURCE_INVENTORY.csv')
    v2 = read(R/'batch10_4f_r1b1b'/'SENTENCE_RESULT_CANDIDATE_CROSSWALK_V2.csv')
    prior = read(R/'batch10_4f_r1b1b'/'CONSOLIDATED_RESULT_LEVEL_EVIDENCE_LEDGER.csv')
    source_urls = {
      'EV-1474':'https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1736902/pdf',
      'EV-1475':'https://revista.ibsp.org.br/index.php/RIBSP/article/download/317/210',
      'EV-1476':'https://periodicorease.pro.br/rease/article/download/19687/11741',
      'EV-1477':'https://www.gov.br/mj/pt-br/assuntos/sua-seguranca/seguranca-publica/aph-tatico/manual-aluno-aph-tatico-mjsp-11-04-2025_compressed.pdf',
      'EV-1479':'https://www.scielo.br/j/ep/a/WKSVkX7LfNVtNHVMMD5hvMC/?lang=pt&format=pdf',
      'EV-1482':'https://revista.forumseguranca.org.br/rbsp/article/download/1764/779',
    }
    # Every assertion below is transcribed from the already recovered primary source.
    # The record status intentionally distinguishes measured effects from descriptive/documentary findings.
    extracted = [
      dict(Evidence_ID='EV-1474', Result_ID='EV-1474-R01', Result_Class='EMPIRICAL_ASSOCIATION', Source_URL=source_urls['EV-1474'], PDF_Page='8', Source_Locator='Table 3; correlation matrix', Population='26 military police officers in the Espírito Santo Officer Training Course (5 women; 21 men)', Study_Design='Cross-sectional correlational study', Outcome='Shooting score and shooting coefficient', Exact_Result='Body mass correlated with score (r=0.410, 95% CI 0.008–0.698, p=0.046) and shooting coefficient (r=0.412, 95% CI 0.010–0.699, p=0.045); BMI correlated with shooting coefficient (r=0.454, 95% CI 0.062–0.724, p=0.025).', Null_or_Contradictory='Most other anthropometric correlations shown in Table 3 were non-significant.', Permitted_Boundary='Association only in this small training-course sample and protocol.', Prohibited_Inference='No causal, universal-readiness, national-prevalence, or BMI-as-proxy inference.', Transferability='Direct Brazilian police-training setting; narrow sample and standardized 5-m shooting protocol.', Integrity_Status='EV1474_PUBLISHER_IDENTITY_PASS; legacy PMCID PMC3382270 rejected.'),
      dict(Evidence_ID='EV-1474', Result_ID='EV-1474-R02', Result_Class='EMPIRICAL_NULL_RESULT', Source_URL=source_urls['EV-1474'], PDF_Page='8', Source_Locator='Table 3; physical activity and physical-fitness rows', Population='26 military police officers in the Espírito Santo Officer Training Course', Study_Design='Cross-sectional correlational study', Outcome='Shooting time, score, and shooting coefficient', Exact_Result='Total, light, moderate and vigorous physical-activity time; push-ups, pull-ups, sit-ups, agility and 2,400-m run did not show statistically significant correlations with the shooting outcomes displayed in Table 3 (all reported p>0.05; push-up score p=0.053).', Null_or_Contradictory='Null results preserved; they limit a broad physical-fitness-to-shooting claim.', Permitted_Boundary='Protocol-specific absence of detected association in this sample.', Prohibited_Inference='No claim that physical fitness improves shooting proficiency generally.', Transferability='Single Brazilian police-training cohort; not independent of EV-1473 cohort family.', Integrity_Status='EV1474_PUBLISHER_IDENTITY_PASS.'),
      dict(Evidence_ID='EV-1474', Result_ID='EV-1474-R03', Result_Class='EMPIRICAL_ASSOCIATION', Source_URL=source_urls['EV-1474'], PDF_Page='8', Source_Locator='Table 3; handgrip and mood rows', Population='26 military police officers in the Espírito Santo Officer Training Course', Study_Design='Cross-sectional correlational study', Outcome='Shooting score', Exact_Result='Dominant handgrip strength correlated with score (r=0.504, 95% CI 0.127–0.754, p=0.011); handgrip in shooting position correlated with score (r=0.431, 95% CI 0.033–0.710, p=0.003); vigor correlated with score (r=0.438, 95% CI 0.061–0.706, p=0.025).', Null_or_Contradictory='Other mood dimensions displayed in Table 3 were non-significant.', Permitted_Boundary='Specific correlations with the study shooting score.', Prohibited_Inference='No prediction, intervention effect, or causal claim.', Transferability='Direct Brazilian police-training setting; requires replication and is one cohort family with EV-1473.', Integrity_Status='EV1474_PUBLISHER_IDENTITY_PASS.'),
      dict(Evidence_ID='EV-1475', Result_ID='EV-1475-R01', Result_Class='DESCRIPTIVE_PRE_POST_RECORD_COUNT', Source_URL=source_urls['EV-1475'], PDF_Page='88', Source_Locator='Results, Graph 2 and accompanying paragraph', Population='REDS occurrences documenting police application of a tourniquet in Minas Gerais', Study_Design='Ex-post-facto descriptive record review', Outcome='Documented tourniquet applications', Exact_Result='The authors report 4 documented applications in 2013–2017 (all civilians) and 194 in 2020–2024 (14, 24, 47, 65, and 44 by year, respectively).', Null_or_Contradictory='No denominator, control group, clinical outcome, or causal counterfactual is reported.', Permitted_Boundary='Descriptive change in documented applications across the stated intervals.', Prohibited_Inference='No survival benefit, effectiveness, or causal attribution to training/normative change.', Transferability='State police record system; documentation practices and case mix may differ elsewhere.', Integrity_Status='Publisher full text verified.'),
      dict(Evidence_ID='EV-1475', Result_ID='EV-1475-R02', Result_Class='DESCRIPTIVE_CASE_MIX', Source_URL=source_urls['EV-1475'], PDF_Page='89', Source_Locator='Results, Table 1 and accompanying paragraph', Population='198 documented tourniquet applications tabulated by recipient', Study_Design='Ex-post-facto descriptive record review', Outcome='Recipient of documented application', Exact_Result='Table 1 reports 13 applications to police officers and 185 to civilians (198 total) across the listed years.', Null_or_Contradictory='The records are limited to documented tourniquet use; they are not all police confrontations or all bleeding events.', Permitted_Boundary='Descriptive recipient distribution in the reviewed records.', Prohibited_Inference='No conclusion about need, benefit, or comparative effectiveness in civilians versus officers.', Transferability='Minas Gerais records only.', Integrity_Status='Publisher full text verified.'),
      dict(Evidence_ID='EV-1475', Result_ID='EV-1475-R03', Result_Class='DESCRIPTIVE_LOGISTICS', Source_URL=source_urls['EV-1475'], PDF_Page='90', Source_Locator='Results, Table 2 and paragraph beginning “No período compreendido”', Population='210 documented tourniquet-use occurrences, 2013–2024', Study_Design='Ex-post-facto descriptive record review', Outcome='Number of tourniquets recorded per attendance', Exact_Result='The authors identified 210 documented occurrences; more than 97% recorded one tourniquet, five recorded two, and none recorded three or more.', Null_or_Contradictory='No clinical effectiveness or adequacy outcome was measured.', Permitted_Boundary='Planning context for recorded device use in this dataset.', Prohibited_Inference='No claim that one kit per vehicle is clinically sufficient or that the device caused better outcomes.', Transferability='Single-state documentation and operational context.', Integrity_Status='Publisher full text verified.'),
      dict(Evidence_ID='EV-1476', Result_ID='EV-1476-R01', Result_Class='NON_EMPIRICAL_CONTEXT', Source_URL=source_urls['EV-1476'], PDF_Page='332', Source_Locator='Methods; description as bibliographic, qualitative and exploratory research', Population='Not an empirical participant sample', Study_Design='Bibliographic qualitative exploratory analysis', Outcome='None measured', Exact_Result='The paper describes itself as a bibliographic, qualitative and exploratory analysis of prehospital tactical care in PMPR special-operations context; no attributable effect estimate or participant outcome was identified.', Null_or_Contradictory='No measured implementation, survival, or performance outcome is reported.', Permitted_Boundary='Contextual description of APH-Tático themes only.', Prohibited_Inference='No effectiveness, survival, or operational-readiness claim.', Transferability='Narrative/context source; not empirical evidence.', Integrity_Status='Publisher full text verified.'),
      dict(Evidence_ID='EV-1479', Result_ID='EV-1479-R01', Result_Class='EMPIRICAL_NULL_RESULT', Source_URL=source_urls['EV-1479'], PDF_Page='15–16', Source_Locator='Results, Table 4 and first Results interpretation paragraph on p.16', Population='One Escola Segura treatment school compared with one control school; survey respondents', Study_Design='Quasi-experimental impact evaluation with regression model', Outcome='Perceived insecurity and reported violence/disorder outcomes', Exact_Result='For the program effect (school×time), Table 4 reports no statistically significant coefficient for insecurity (0.06, SE 0.09), verbal aggression (0.17, 0.11), physical aggression (0.02, 0.06), sexual offenses (-0.01, 0.07), theft/robbery (0.19, 0.10), graffiti (0.12, 0.08), or illicit-drug perception (0.12, 0.06). The authors state no evidence that outcomes changed because of police presence.', Null_or_Contradictory='The sexual-offense coefficient was in the expected direction but non-significant.', Permitted_Boundary='Null finding for the evaluated school/program/time and reported outcomes.', Prohibited_Inference='No claim that police presence improves school safety generally.', Transferability='One-school evaluation; short follow-up and setting-specific implementation.', Integrity_Status='SciELO full text verified.'),
      dict(Evidence_ID='EV-1482', Result_ID='EV-1482-R01', Result_Class='DOCUMENTARY_IMPLEMENTATION_FINDING', Source_URL=source_urls['EV-1482'], PDF_Page='199, 203–205', Source_Locator='Methods; SWOT analysis and Results/Discussion', Population='PMPI CAIS institutional documents and open information', Study_Design='Qualitative exploratory documentary case study', Outcome='Planning barriers and proposed mental-health policy design', Exact_Result='The authors describe document-derived constraints for the PMPI CAIS, including insufficient staff, professional training and physical structure, and use SWOT/4-actions/Canvas/5W2H to formulate a proposed policy plan.', Null_or_Contradictory='No implemented-program outcome, effectiveness estimate, or participant health outcome is reported.', Permitted_Boundary='Documentary planning context for a PMPI mental-health policy proposal.', Prohibited_Inference='No claim that the proposed program improves mental health, readiness, or service outcomes.', Transferability='Single institutional case and proposal, not evaluated implementation.', Integrity_Status='Publisher full text verified.'),
    ]
    result_fields=list(extracted[0])
    write(O/'VERIFIED_SOURCE_RESULT_EXTRACTION.csv', result_fields, extracted)
    write(O/'NEW_RESULT_LEVEL_EVIDENCE_LEDGER.csv', result_fields, extracted)
    loc=[{k:x[k] for k in ['Evidence_ID','Result_ID','Source_URL','PDF_Page','Source_Locator','Result_Class']} for x in extracted]
    write(O/'NEW_RESULT_SOURCE_LOCATORS.csv', list(loc[0]), loc)
    boundary=[{k:x[k] for k in ['Evidence_ID','Result_ID','Permitted_Boundary','Prohibited_Inference']} for x in extracted]
    write(O/'RESULT_LEVEL_CLAIM_BOUNDARIES.csv', list(boundary[0]), boundary)
    trans=[{k:x[k] for k in ['Evidence_ID','Result_ID','Population','Study_Design','Transferability']} for x in extracted]
    write(O/'RESULT_LEVEL_TRANSFERABILITY.csv', list(trans[0]), trans)
    nulls=[{k:x[k] for k in ['Evidence_ID','Result_ID','Null_or_Contradictory']} for x in extracted if x['Null_or_Contradictory']]
    write(O/'NULL_RESULT_COMPLETENESS_AUDIT.csv', list(nulls[0]), nulls)
    ident=[dict(Evidence_ID='EV-1474', Publisher='Frontiers in Psychology', Publisher_URL='https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1736902/full', Publisher_Title='Correlation between physical fitness, psychophysiological parameters and performance in a firearm proficiency test in military police officers', V013_DOCX_Title='Correlation between physical fitness, psychophysiological parameters and performance in a firearm proficiency test in military police officers', Authors='Junger; de Oliveira; Viana; Pinheiro; Fortes Junior; Rica; Bullo; Gobbo; Bergamin; Bocalini', DOI='10.3389/fpsyg.2025.1736902', Journal='Frontiers in Psychology', Publisher_Display_Date='2026-01-30', PMID='41694750', PMID_Source='PubMed/NCBI record retrieved 2026-10-07', Article_Identifier='1736902', Legacy_PMCID='PMC3382270', Legacy_PMCID_Status='REJECTED_NOT_THIS_ARTICLE', Identity_Status='EV1474_PUBLISHER_IDENTITY_PASS', Reconciliation_Note='The frozen inventory carries a stale working title; the v0.13 DOCX bibliography, publisher record, DOI, authors and PMID reconcile. PubMed publication year 2025 reflects electronic indexing; publisher display date and v0.13 citation are 2026. No manuscript or metadata edit was made.')]
    write(O/'EV1474_PUBLISHER_IDENTITY_VALIDATION.csv',list(ident[0]),ident)
    cohort=[dict(Evidence_ID='EV-1474', Cohort_Family='CF-BR-PMES-CFO-2023-01', Related_Evidence_ID='EV-1473', Relationship='PARTIAL_OVERLAP', Independent_Cohort_Count='1', Evidence='Shared PMES officer-training context; prior project governance classification retained.', Rule='Do not count EV-1473 and EV-1474 as independent replications.', Change_To_CEF_V1='NO')]
    write(O/'EV1474_COHORT_RELATIONSHIP.csv',list(cohort[0]),cohort)
    guide=[dict(Evidence_ID='EV-1477', Guidance_ID='EV-1477-G01', Source_URL=source_urls['EV-1477'], PDF_Page='137', Locator='5.1 Diretriz de atendimento sob confronto armado', Guidance='For limb bleeding during armed confrontation, the manual directs application of a tourniquet and subsequent transition to care phases after movement from the risk area.', Source_Type='Official MJSP operational guidance', Empirical_Result='NONE', Permitted_Use='Guidance/context only', Prohibited_Use='No effect, survival, comparative or causal claim.'),dict(Evidence_ID='EV-1477', Guidance_ID='EV-1477-G02', Source_URL=source_urls['EV-1477'], PDF_Page='138–142', Locator='Tactical field care and tactical evacuation directives', Guidance='The manual sets care priorities including massive hemorrhage, airway, respiration, circulation/shock/hypothermia and evacuation.', Source_Type='Official MJSP operational guidance', Empirical_Result='NONE', Permitted_Use='Guidance/context only', Prohibited_Use='No effect, survival, comparative or causal claim.')]
    write(O/'EV1477_GUIDANCE_EXTRACTION.csv',list(guide[0]),guide)
    extract_by=defaultdict(list)
    for r in extracted: extract_by[r['Evidence_ID']].append(r['Result_ID'])
    full={'EV-1473','EV-1474','EV-1475','EV-1476','EV-1479','EV-1482','EV-1484'}
    gov={'EV-1477'}; abstracts={'EV-1471','EV-1481'}
    packets=[]; insuff=[]
    for x in inv:
        ev=x['Evidence_ID']
        depth='FULL_TEXT_VERIFIED' if ev in full else ('GOVERNMENT_FULL_SOURCE_VERIFIED' if ev in gov else ('ABSTRACT_RESULT_ONLY' if ev in abstracts else 'SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT'))
        status='RESULT_LOCALIZED' if ev in extract_by else ('GUIDANCE_SEPARATED' if ev=='EV-1477' else ('PRIOR_RESULT_LOCALIZED' if ev in {'EV-1473','EV-1484'} else ('ABSTRACT_RESULT_ONLY' if ev in abstracts else 'SOURCE_INSUFFICIENT')))
        packets.append(dict(Reference_ID=x['Reference_ID'],Evidence_ID=ev,Source_Depth=depth,Result_Packet_Status=status,New_Result_IDs=';'.join(extract_by[ev]) or 'NONE',Source_URL=source_urls.get(ev,'See upstream verified source provenance'),Identity_Status='EV1474_PUBLISHER_IDENTITY_PASS' if ev=='EV-1474' else 'UNCHANGED_OR_NOT_APPLICABLE',Sentence_Adjudication='NOT_PERFORMED_IN_R1B1C',Notes='No manuscript, Zotero, CEF-v1 or reference-set mutation.'))
        if depth=='SOURCE_INSUFFICIENT_FOR_RESULT_LEVEL_SUPPORT': insuff.append(dict(Reference_ID=x['Reference_ID'],Evidence_ID=ev,Reason='No lawful full text or structured abstract result packet recovered in the frozen recovery scope.',Current_Status='SOURCE_INSUFFICIENT_FINAL_FOR_R1B1C',Allowed_Use='No result-level scientific support',Required_Future_Action='Obtain a lawful verifiable source before sentence-level support adjudication.'))
    write(O/'REFERENCE_PACKET_STATUS_V3.csv',list(packets[0]),packets)
    write(O/'SOURCE_INSUFFICIENT_FINAL_FOR_R1B1C.csv',list(insuff[0]),insuff)
    # Preserve the pre-existing crosswalk row identities and never set an adjudication disposition here.
    cross=[]
    for row in v2:
        eids=[e for e in row['Evidence_ID'].split(';') if e]
        additions=[rid for ev in eids for rid in extract_by.get(ev,[])]
        cross.append(dict(Sentence_ID=row['Sentence_ID'],Existing_Reference_Number=row['Existing_Reference_Number'],Existing_Reference_ID=row['Existing_Reference_ID'],Evidence_ID=row['Evidence_ID'],Prior_Candidate_Result_ID=row['Candidate_Result_ID'],New_Candidate_Result_ID=';'.join(additions) or 'NONE',Result_Extraction_Status='CANDIDATE_MAP_ONLY—NOT_SENTENCE_READJUDICATED',Adjudication_Status='UNCHANGED; NOT PERFORMED IN R1B1C'))
    write(O/'SENTENCE_RESULT_CANDIDATE_CROSSWALK_V3.csv',list(cross[0]),cross)
    files=[O/f for f in ['VERIFIED_SOURCE_RESULT_EXTRACTION.csv','NEW_RESULT_LEVEL_EVIDENCE_LEDGER.csv','NEW_RESULT_SOURCE_LOCATORS.csv','RESULT_LEVEL_CLAIM_BOUNDARIES.csv','RESULT_LEVEL_TRANSFERABILITY.csv','NULL_RESULT_COMPLETENESS_AUDIT.csv','EV1474_PUBLISHER_IDENTITY_VALIDATION.csv','EV1474_COHORT_RELATIONSHIP.csv','EV1477_GUIDANCE_EXTRACTION.csv','REFERENCE_PACKET_STATUS_V3.csv','SENTENCE_RESULT_CANDIDATE_CROSSWALK_V3.csv','SOURCE_INSUFFICIENT_FINAL_FOR_R1B1C.csv']]
    manifest=dict(batch='BATCH 10.4F-R1B1C', gate='VERIFIED_SOURCE_RESULT_EXTRACTION_PASS', extraction_scope='Five newly recovered full texts plus EV-1477 guidance; no sentence re-adjudication.', full_texts_extracted_and_localized=5, result_records=len(extracted), empirical_result_records=7, non_empirical_context_records=2, guidance_records=len(guide), EV1474_identity='EV1474_PUBLISHER_IDENTITY_PASS', EV1474_legacy_pmcid='REJECTED', source_insufficient=len(insuff), sentence_re_adjudication=0, manuscript_changes=0, zotero_changes=0, cef_v1_changes=0, forced_semantic_links=0, deterministic_regeneration='python analysis/build_batch10_4f_r1b1c.py', artifact_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
    (O/'BATCH10_4F_R1B1C_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    report=f'''# BATCH 10.4F-R1B1C — verified source result extraction

## Gate

`VERIFIED_SOURCE_RESULT_EXTRACTION_PASS`

This gate completes result-level extraction and locator recovery for the five recovered full texts: EV-1474, EV-1475, EV-1476, EV-1479 and EV-1482. It separates the official MJSP manual (EV-1477) as guidance, not empirical evidence. It does **not** readjudicate any sentence, alter either manuscript, change Zotero, modify CEF-v1, change a frozen claim, or promote Claim-Ready status.

## Evidence status

- **9** new records have a result-level or explicitly non-empirical/documentary status with an auditable PDF locator.
- **7** records contain empirical findings, including preserved null results for EV-1474 and EV-1479.
- **2** are bounded non-empirical context/documentary records (EV-1476 and EV-1482); neither is treated as effectiveness evidence.
- EV-1477 has **2** guidance records and no empirical result.
- **6/16** frozen-reference packets remain source-insufficient and are isolated in `SOURCE_INSUFFICIENT_FINAL_FOR_R1B1C.csv`.

## EV-1474 identity control

The official Frontiers record, v0.13 DOCX bibliography, DOI `10.3389/fpsyg.2025.1736902`, author list, journal, article identifier `1736902`, and PubMed PMID `41694750` reconcile. The old inventory's working title is stale; no historical metadata was overwritten. Publisher display date is 2026-01-30 while PubMed carries a 2025 electronic-publication year; this is documented as version dating, not treated as an identity conflict. `PMC3382270` remains explicitly rejected.

EV-1474 remains within cohort family `CF-BR-PMES-CFO-2023-01` with EV-1473 and does not represent an independent replication.

## Guardrails retained

All reported associations are bounded by the source design and population. Descriptive use counts are not interpreted as survival benefit or training effectiveness. The school-program null result is retained. Guidance is not promoted to outcome evidence. No sentence-to-result link was adjudicated in this batch.

## Reproducibility

Run `python analysis/build_batch10_4f_r1b1c.py`, then `python -m pytest` and `git diff --check`.
'''
    (O/'BATCH10_4F_R1B1C_REPORT.md').write_text(report,encoding='utf-8')

if __name__ == '__main__':
    main()
