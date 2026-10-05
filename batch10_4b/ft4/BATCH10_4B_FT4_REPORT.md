# Batch 10.4B-FT4 — high-impact verified full-text appraisal

## Scope and provenance

Only EV-1462, EV-1463 and EV-1466 were read.  The assessment used the distinct final publisher/Scielo routes recorded in FT3R and did not reuse the invalid shared-PMCID/XML association.  Each route was previously HTTP-200, title/DOI/year matched and SHA-256 documented.

## Results

All 3/3 records now have structured Methods/Results extraction, design confirmation, appraisal, risk-of-bias status, claim mapping, transferability assessment and an AI-provisional decision.  EV-1462 is a seven-trial military sleep-loss caffeine meta-analysis (AMSTAR 2: LOW) and is a `PROVISIONAL_REPLACE_CANDIDATE`, not a replacement. EV-1463 is a 436-participant PMDF cross-sectional clinical cohort (JBI: SOME_CONCERNS) and is `PROVISIONAL_INCLUDE` solely for bounded surveillance context. EV-1466 is a 261-person Bahia cross-sectional ROC study (JBI: HIGH_RISK_OF_BIAS) and is `CONTEXT_ONLY`; its AUC 0.58 cutoffs do not demonstrate prevention.

The integral ledgers preserve null/qualifying results: EV-1462 does not establish universal operational benefit; EV-1463 did not find significant role/shift differences; EV-1466 has weak discrimination and no causal model.  No record is Claim-Ready and human confirmation remains pending.

## Integrity and controls

FT4 observed no correction, erratum, retraction or expression-of-concern notice on the versioned source pages. This is recorded as an observation, **not** database-wide integrity clearance. No Zotero, CEF-v1, manuscript, canonical universe or other queue record was modified.

## Gate and next path

`HIGH3_FULL_TEXT_APPRAISAL_COMPLETE` is satisfied as a technical documentation gate (3/3 appraised). It is not `REFERENCE_SATURATION_PASS`, final inclusion, scientific approval or authorization for v0.13.

Recommended next path: **A — `TARGETED_HIGH_ACCESS_REMEDIATION_REQUIRED`**. Twenty-two HIGH and three contradictory candidates remain access-blocked, so attempting only MEDIUM records would risk leaving high-value/contradictory evidence unresolved before saturation work.

## Red-team findings

The review retained provenance segregation, did not elevate systematic-review prestige over primary-study limitations, did not convert cross-sectional/ROC associations to causal prevention claims, and preserved no-difference/null findings.
