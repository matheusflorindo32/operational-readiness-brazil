"""Materialize the audited FT4 appraisal of the three verified High-impact records.

This builder deliberately contains only observations traceable to the three
publisher routes verified in FT3R.  It does not promote a record to a final
reference, amend a manuscript, or write to Zotero.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4b" / "ft4"
OUT.mkdir(parents=True, exist_ok=True)
IDS = ("EV-1462", "EV-1463", "EV-1466")
SOURCES = {
    "EV-1462": "https://www.frontiersin.org/articles/10.3389/fnut.2026.1893033/full",
    "EV-1463": "https://www.frontiersin.org/articles/10.3389/fpubh.2025.1716547/full",
    "EV-1466": "https://www.scielo.br/j/brjp/a/7QzX6dJgmZdQg8fhmPNvPyq/?lang=en",
}


def write_csv(name: str, headers: list[str], rows: list[dict[str, str]]) -> None:
    with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    extraction = [
        {
            "Evidence_ID": "EV-1462", "DOI": "10.3389/fnut.2026.1893033",
            "Title": "Acute caffeine supplementation as a nutrition-based strategy to mitigate sleep-loss-related cognitive and operational performance impairments in military personnel: a systematic review and meta-analysis",
            "Source_URL": SOURCES["EV-1462"], "Full_text_sections_read": "Methods 2.1-2.7; Results 3.1-3.4; Discussion; funding/COI statements",
            "Design": "Systematic review and meta-analysis of randomized, double-blind, placebo-controlled trials",
            "Population": "Military personnel or military-related populations under sleep deprivation, sleep restriction, or sustained wakefulness",
            "Sample": "7 included trials; aggregate participant count NR — NOT REPORTED in the article text reviewed",
            "Exposure_intervention": "Acute caffeine; most reported doses 200-400 mg; timing/regimens varied",
            "Comparator": "Placebo or non-caffeinated control", "Outcomes": "Vigilance/response, complex cognition, military-task performance",
            "Methods_results": "Six databases searched inception to 15-Mar-2026; PROSPERO CRD420261375742; duplicate selection/extraction; RoB assessed; random-effects meta-analysis.",
            "Main_results": "Vigilance/response SMD 0.73 (95% CI 0.50-0.96; I2 0.0%); complex cognition SMD 0.54 (0.16-0.93; I2 0.0%); military task performance SMD 0.45 (0.19-0.71; I2 29.2%).",
            "Null_or_qualifying_results": "Benefits were task-dependent; precision shooting was not consistently improved. Only 1/7 studies low RoB, 5/7 some concerns, 1/7 high RoB; dose, timing, habitual caffeine use, task and sleep-loss models varied.",
            "Limitations": "Small evidence base; limited moderator analysis and publication-bias power; heterogeneous tasks/exposures; uncertain generalizability to female and conventional-force personnel.",
            "Funding_COI": "No financial support declared; authors declared no commercial/financial COI; generative AI use for language/presentation declared.",
            "Claim_boundary": "May support a carefully bounded claim that acute caffeine can partially mitigate selected sleep-loss performance decrements in studied military settings; it does not show that caffeine resolves sleep loss or improves every operational outcome.",
        },
        {
            "Evidence_ID": "EV-1463", "DOI": "10.3389/fpubh.2025.1716547",
            "Title": "Cardiovascular risk factors across job roles and work shifts in a Brazilian Military Police cohort: a cross-sectional study",
            "Source_URL": SOURCES["EV-1463"], "Full_text_sections_read": "Methods 2.1-2.4; Results 3.1-3.3; Discussion 4.5; funding/COI statements",
            "Design": "Cross-sectional observational study", "Population": "Active-duty male Federal District Military Police officers aged >40 years without known atherosclerotic disease",
            "Sample": "436 volunteers assessed Sep-2021 to Apr-2024 (456 assessed; 10 statin users and 10 with missing functional data excluded)",
            "Exposure_intervention": "Administrative versus operational assignment; 6h/day, 12/36, 12/60 and 24/72 schedules", "Comparator": "Role and schedule strata",
            "Outcomes": "Six-metric adapted cardiovascular health score and clinical/laboratory cardiometabolic factors",
            "Methods_results": "Board-certified cardiologist assessment, laboratory tests and REDCap data; chi-square/Mann-Whitney/Kruskal-Wallis; MICE for continuous missing data.",
            "Main_results": "Median age 46.0; 81.1% overweight/obese and 95% elevated blood pressure/hypertension; nearly 90% moderate/high cardiovascular risk and 3% ideal metrics. No statistically significant role or shift differences were reported.",
            "Null_or_qualifying_results": "No statistically significant differences between job roles or work schedules; numerical schedule patterns are not confirmatory.",
            "Limitations": "Cross-sectional design precludes causal inference; voluntary convenience sample risks selection bias and limits generalizability; women and younger officers were outside the sampled population.",
            "Funding_COI": "In-kind laboratory support from Sabin; FAPDF publication support disclosed; authors declared no commercial/financial COI.",
            "Claim_boundary": "Supports surveillance of cardiometabolic risk in this sampled Brazilian military-police cohort, not causal attribution to role/shift or prevalence claims for all Brazilian public-safety institutions.",
        },
        {
            "Evidence_ID": "EV-1466", "DOI": "10.63231/2595-0118.e202684-en",
            "Title": "Leisure-time physical activity as a discriminator of the absence of musculoskeletal pain in military police officers",
            "Source_URL": SOURCES["EV-1466"], "Full_text_sections_read": "Methods; Instruments and variables; Statistical analysis; Results; Limitations; COI statement",
            "Design": "Cross-sectional diagnostic-discrimination (ROC) analysis", "Population": "Military police from four units in Jequié, Bahia, Brazil",
            "Sample": "261 officers (43.8 ± 7.4 years; 79.0% men), probability sampled from target population of 601",
            "Exposure_intervention": "Leisure-time physical activity, long IPAQ; walking, moderate, vigorous and combined MVPA", "Comparator": "Presence/absence of 12-month musculoskeletal pain on NMQ",
            "Outcomes": "ROC discrimination of absence of musculoskeletal pain", "Methods_results": "ROC/AUC, sensitivity, specificity and Youden cutoffs using Stata 16; no causal model.",
            "Main_results": "Low-back pain prevalence 48.0%. Absence of low-back pain: vigorous activity 140 min/week, AUC 0.58, sensitivity 58%, specificity 57%; MVPA 270 min/week, AUC 0.58, sensitivity 48%, specificity 66%.",
            "Null_or_qualifying_results": "The reported AUCs indicate weak discrimination; no causal prevention estimate, intervention effect, or external validation was reported.",
            "Limitations": "Single-region sample; cross-sectional design; self-reported pain/activity; ROC cutoffs are not prevention thresholds and require external validation.",
            "Funding_COI": "Funding NR — NOT REPORTED in the source text reviewed; conflict of interests: none declared.",
            "Claim_boundary": "May contextualize low-back-pain burden and weak cross-sectional discrimination in the studied force; cannot support that physical activity prevents pain or that the cutoffs should be implemented as clinical/operational targets.",
        },
    ]
    headers = list(extraction[0])
    write_csv("HIGH3_FULL_TEXT_EXTRACTION.csv", headers, extraction)

    appraisal = [
        {"Evidence_ID":"EV-1462","Instrument":"AMSTAR 2","Domain_judgments":"PICO YES; protocol YES (PROSPERO); search PARTIAL (six databases/inception/date, full strategies supplementary; gray literature NR); duplicate selection/extraction YES; RoB assessment YES but published reporting leaves application details limited; meta-analysis YES; heterogeneity YES; publication bias PARTIAL because seven studies; excluded-study list NR.","Overall_judgment":"LOW","Rationale":"Prospectively registered, duplicate workflow and quantitative synthesis are documented, but the small base and reporting limitations require cautious use; review-level appraisal does not erase primary-study RoB.","Human_review":"PENDING"},
        {"Evidence_ID":"EV-1463","Instrument":"JBI Analytical Cross-Sectional Checklist","Domain_judgments":"Inclusion YES; setting/subjects YES; role/schedule exposure YES; outcomes YES (clinical/laboratory); confounders NO; confounder strategy NO; outcome measurement YES; analysis PARTIAL (unadjusted group comparisons and MICE described).","Overall_judgment":"SOME_CONCERNS","Rationale":"Objective clinical measurement is a strength, but convenience volunteers, restriction to male >40 officers and no confounder-adjusted association model limit inference.","Human_review":"PENDING"},
        {"Evidence_ID":"EV-1466","Instrument":"JBI Analytical Cross-Sectional Checklist plus ROC interpretation boundary","Domain_judgments":"Inclusion YES; setting/subjects YES; exposure PARTIAL (validated self-report IPAQ); outcome PARTIAL (validated self-report NMQ); confounders NO; confounder strategy NO; outcome measurement PARTIAL; analysis PARTIAL (ROC/Youden without causal model or external validation).","Overall_judgment":"HIGH_RISK_OF_BIAS","Rationale":"Cross-sectional self-report data, no confounding control and low, internally derived ROC discrimination preclude causal or threshold-use inference.","Human_review":"PENDING"},
    ]
    write_csv("HIGH3_APPRAISAL_LEDGER.csv", list(appraisal[0]), appraisal)
    rob = [{"Evidence_ID": x["Evidence_ID"], "Selection_bias": "See appraisal rationale", "Confounding": "Unresolved/No control" if x["Evidence_ID"] != "EV-1462" else "Primary-study variation; review reports 5 some-concerns and 1 high RoB", "Measurement_bias": "See appraisal rationale", "Missing_data": "NR — NOT REPORTED" if x["Evidence_ID"] == "EV-1466" else "See full-text appraisal", "Selective_reporting": "Potential/limited reporting", "Overall": x["Overall_judgment"], "No_claim_ready": "YES"} for x in appraisal]
    write_csv("HIGH3_RISK_OF_BIAS_LEDGER.csv", list(rob[0]), rob)
    results = [{"Evidence_ID": x["Evidence_ID"], "Source_locator": x["Full_text_sections_read"], "Result": x["Main_results"], "Null_or_boundary": x["Null_or_qualifying_results"], "Exact_claim_limit": x["Claim_boundary"]} for x in extraction]
    write_csv("HIGH3_RESULTS_LEDGER.csv", list(results[0]), results)
    claims = [
        {"Evidence_ID":"EV-1462","Manuscript":"International","Section":"Sleep/recovery and cognitive readiness","Potential_claim":"Acute caffeine can partially mitigate selected sleep-loss-related vigilance and performance decrements in military settings.","Support":"PARTIAL_SUPPORT","Directness":"MODERATELY_DIRECT","Locator":"Results 3.4; Discussion limitations","Wording_constraint":"Do not state that caffeine resolves sleep loss, improves all tasks, or transfers automatically to Brazilian police.","Human_review":"PENDING"},
        {"Evidence_ID":"EV-1463","Manuscript":"Brazil","Section":"Medical/cardiovascular readiness","Potential_claim":"The sampled PMDF cohort had a high measured cardiometabolic-risk burden supporting surveillance consideration.","Support":"PARTIAL_SUPPORT","Directness":"DIRECT","Locator":"Methods 2.1-2.4; Results 3.1-3.3; Limitations 4.5","Wording_constraint":"Do not generalize to all forces or attribute risk to roles/shifts.","Human_review":"PENDING"},
        {"Evidence_ID":"EV-1466","Manuscript":"Brazil","Section":"Musculoskeletal health","Potential_claim":"In one Bahia military-police sample, low-back pain was common and leisure-time activity had weak cross-sectional ROC discrimination for absence of pain.","Support":"CONTEXT_ONLY","Directness":"DIRECT","Locator":"Methods; Statistical analysis; Results; Limitations","Wording_constraint":"Do not translate ROC cutoffs into causal prevention or operational targets.","Human_review":"PENDING"},
    ]
    write_csv("HIGH3_CLAIM_CITATION_MATRIX.csv", list(claims[0]), claims)
    decisions = [
        {"Evidence_ID":"EV-1462","Study_Design":"Systematic review and meta-analysis","Appraisal_Instrument":"AMSTAR 2","Appraisal_Overall_AI":"LOW","Risk_of_Bias_AI":"PRIMARY_STUDIES: 1 LOW, 5 SOME_CONCERNS, 1 HIGH","Citation_Fitness":"PARTIAL_SUPPORT","Directness":"MODERATELY_DIRECT","Provisional_Decision":"PROVISIONAL_REPLACE_CANDIDATE","CLAIM_READY_PROVISIONAL":"NO","HUMAN_CONFIRMATION":"PENDING","Claim_Role":"Bounded sleep-loss caffeine mitigation claim only; no universal benefit claim.","Transferability":"International military context; Brazil applicability requires separate contextual validation.","Integrity_Status":"NO_NOTICE_OBSERVED_ON_VERSIONED_SOURCE_NOT_DATABASE_WIDE_CLEARANCE","FCR_CANDIDATE_FULL_TEXT_SUPPORTED":"NO","Decision_Rationale":"Military sleep-loss RCT synthesis with quantified effects, but small base/primary-study RoB and integrity screening remains bounded."},
        {"Evidence_ID":"EV-1463","Study_Design":"Cross-sectional study","Appraisal_Instrument":"JBI Analytical Cross-Sectional Checklist","Appraisal_Overall_AI":"SOME_CONCERNS","Risk_of_Bias_AI":"SELECTION/CONFOUNDING CONCERNS","Citation_Fitness":"PARTIAL_SUPPORT","Directness":"DIRECT","Provisional_Decision":"PROVISIONAL_INCLUDE","CLAIM_READY_PROVISIONAL":"NO","HUMAN_CONFIRMATION":"PENDING","Claim_Role":"Bounded PMDF cardiometabolic surveillance context; not causal role/shift evidence.","Transferability":"Direct to the sampled PMDF setting only; not generalizable to all public-safety forces.","Integrity_Status":"NO_NOTICE_OBSERVED_ON_VERSIONED_SOURCE_NOT_DATABASE_WIDE_CLEARANCE","FCR_CANDIDATE_FULL_TEXT_SUPPORTED":"NO","Decision_Rationale":"Direct Brazilian police clinical surveillance data, bounded by convenience sampling, demographic restriction and non-causal design."},
        {"Evidence_ID":"EV-1466","Study_Design":"Cross-sectional ROC study","Appraisal_Instrument":"JBI Analytical Cross-Sectional Checklist plus ROC interpretation boundary","Appraisal_Overall_AI":"HIGH_RISK_OF_BIAS","Risk_of_Bias_AI":"SELF_REPORT/CONFOUNDING/NO_EXTERNAL_VALIDATION","Citation_Fitness":"CONTEXT_ONLY","Directness":"DIRECT","Provisional_Decision":"CONTEXT_ONLY","CLAIM_READY_PROVISIONAL":"NO","HUMAN_CONFIRMATION":"PENDING","Claim_Role":"Weak ROC discrimination context only; no prevention threshold claim.","Transferability":"Direct to sampled Bahia military police only; regional/institutional transferability uncertain.","Integrity_Status":"NO_NOTICE_OBSERVED_ON_VERSIONED_SOURCE_NOT_DATABASE_WIDE_CLEARANCE","FCR_CANDIDATE_FULL_TEXT_SUPPORTED":"NO","Decision_Rationale":"Direct Brazilian context but weak, unvalidated cross-sectional ROC evidence cannot support prevention/threshold claims."},
    ]
    write_csv("HIGH3_PROVISIONAL_DECISIONS.csv", list(decisions[0]), decisions)
    replacement = [{"Candidate_Evidence_ID":"EV-1462","Current_Related_Evidence":"EV-1471; EV-1472","Scope":"Caffeine/sleep-loss performance in military personnel","Current_reference_appraisal":"Not re-appraised in FT4","Candidate_appraisal":"AMSTAR 2 LOW; 7 trials with quantified domain effects","Incremental_value":"HIGH","Comparison_decision":"REPLACE_CURRENT_PROVISIONAL","Rationale":"More directly targeted, quantitative and recent synthesis; replacement is not executed and requires claim-level comparison plus human confirmation."}]
    write_csv("HIGH3_REPLACEMENT_COMPARISON.csv", list(replacement[0]), replacement)
    overlap = [
        {"Evidence_ID":"EV-1462","Overlap_status":"POSSIBLE_TOPIC_OVERLAP","Incremental_value":"HIGH","Rationale":"Potential overlap with current caffeine references; not a study-cohort duplicate."},
        {"Evidence_ID":"EV-1463","Overlap_status":"NO_DIRECT_OVERLAP_IDENTIFIED","Incremental_value":"HIGH","Rationale":"Distinct PMDF clinical cohort; no shared cohort asserted."},
        {"Evidence_ID":"EV-1466","Overlap_status":"POSSIBLE_BRAZILIAN_POLICE_DOMAIN_OVERLAP","Incremental_value":"MODERATE","Rationale":"Distinct ESTOP/Jequie dataset; context is direct but evidence is weak for intervention claims."},
    ]
    write_csv("HIGH3_OVERLAP_LEDGER.csv", list(overlap[0]), overlap)
    transfer = [
        {"Evidence_ID":"EV-1462","International":"MODERATELY_DIRECT to sleep-loss military context","Brazil":"INDIRECT; Brazilian police implementation needs separate validation","Boundary":"No universal caffeine protocol or sleep-loss substitute."},
        {"Evidence_ID":"EV-1463","International":"INDIRECT; male PMDF sample only","Brazil":"DIRECT to sampled PMDF setting; limited for women, younger officers and other forces","Boundary":"No causal role/shift inference."},
        {"Evidence_ID":"EV-1466","International":"VERY_INDIRECT outside Brazilian military police","Brazil":"DIRECT to sampled Bahia force; uncertain across regions/institutions","Boundary":"No prevention threshold or causal interpretation."},
    ]
    write_csv("HIGH3_TRANSFERABILITY_LEDGER.csv", list(transfer[0]), transfer)
    integrity = [{"Evidence_ID": ev, "DOI_title_version":"Verified against FT3R official route", "Source_checked":"Publisher/Scielo versioned full-text page", "Correction_erratum_retraction_EOC":"No notice observed on page during FT4; this is not a database-wide clearance", "Status":"NO_NOTICE_OBSERVED_ON_VERSIONED_SOURCE_NOT_DATABASE_WIDE_CLEARANCE", "Decision_effect":"No Claim-Ready or final inclusion; human confirmation remains required."} for ev in IDS]
    write_csv("HIGH3_INTEGRITY_LEDGER.csv", list(integrity[0]), integrity)
    fcr = [{"Evidence_ID": ev, "FCR_CANDIDATE_FULL_TEXT_SUPPORTED":"NO", "Reason":"CEF-v1 remains unchanged; no freeze-change request is generated in FT4."} for ev in IDS]
    write_csv("HIGH3_FCR_CANDIDATES.csv", list(fcr[0]), fcr)

    report = """# Batch 10.4B-FT4 — high-impact verified full-text appraisal\n\n## Scope and provenance\n\nOnly EV-1462, EV-1463 and EV-1466 were read.  The assessment used the distinct final publisher/Scielo routes recorded in FT3R and did not reuse the invalid shared-PMCID/XML association.  Each route was previously HTTP-200, title/DOI/year matched and SHA-256 documented.\n\n## Results\n\nAll 3/3 records now have structured Methods/Results extraction, design confirmation, appraisal, risk-of-bias status, claim mapping, transferability assessment and an AI-provisional decision.  EV-1462 is a seven-trial military sleep-loss caffeine meta-analysis (AMSTAR 2: LOW) and is a `PROVISIONAL_REPLACE_CANDIDATE`, not a replacement. EV-1463 is a 436-participant PMDF cross-sectional clinical cohort (JBI: SOME_CONCERNS) and is `PROVISIONAL_INCLUDE` solely for bounded surveillance context. EV-1466 is a 261-person Bahia cross-sectional ROC study (JBI: HIGH_RISK_OF_BIAS) and is `CONTEXT_ONLY`; its AUC 0.58 cutoffs do not demonstrate prevention.\n\nThe integral ledgers preserve null/qualifying results: EV-1462 does not establish universal operational benefit; EV-1463 did not find significant role/shift differences; EV-1466 has weak discrimination and no causal model.  No record is Claim-Ready and human confirmation remains pending.\n\n## Integrity and controls\n\nFT4 observed no correction, erratum, retraction or expression-of-concern notice on the versioned source pages. This is recorded as an observation, **not** database-wide integrity clearance. No Zotero, CEF-v1, manuscript, canonical universe or other queue record was modified.\n\n## Gate and next path\n\n`HIGH3_FULL_TEXT_APPRAISAL_COMPLETE` is satisfied as a technical documentation gate (3/3 appraised). It is not `REFERENCE_SATURATION_PASS`, final inclusion, scientific approval or authorization for v0.13.\n\nRecommended next path: **A — `TARGETED_HIGH_ACCESS_REMEDIATION_REQUIRED`**. Twenty-two HIGH and three contradictory candidates remain access-blocked, so attempting only MEDIUM records would risk leaving high-value/contradictory evidence unresolved before saturation work.\n\n## Red-team findings\n\nThe review retained provenance segregation, did not elevate systematic-review prestige over primary-study limitations, did not convert cross-sectional/ROC associations to causal prevention claims, and preserved no-difference/null findings.\n"""
    (OUT / "BATCH10_4B_FT4_REPORT.md").write_text(report, encoding="utf-8")
    outputs = sorted(path for path in OUT.iterdir() if path.name != "BATCH10_4B_FT4_MANIFEST.json")
    manifest = {"batch":"BATCH10_4B_FT4", "gate":"HIGH3_FULL_TEXT_APPRAISAL_COMPLETE", "processed_ids":list(IDS), "count":3, "claim_ready":0, "human_review":0, "cef_v1":"UNCHANGED", "zotero":"UNCHANGED", "manuscript":"UNCHANGED", "sources":SOURCES, "files": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in outputs}}
    (OUT / "BATCH10_4B_FT4_MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
