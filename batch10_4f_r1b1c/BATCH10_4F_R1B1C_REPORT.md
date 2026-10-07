# BATCH 10.4F-R1B1C — verified source result extraction

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
