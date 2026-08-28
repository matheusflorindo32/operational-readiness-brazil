# PubMed A/B/C Production Audit — 2026-08-28

## Decision

**PUBMED: BLOCKED.** Search execution, export, deterministic staging
normalization, cross-family deduplication, and article-level workbook entry are
complete. The gate cannot pass until the production RIS is imported and audited
for duplicates in the real local Zotero Desktop library.

## Baseline and protocol audit

- Git baseline: `68038963bbc4c0cb0db8c2bdd5f0dfe04cd23bd8`.
- Design retained: conceptual and applied scientific essay informed by structured
  and reproducible evidence identification; not a systematic or scoping review.
- Evidence families retained: A core readiness/performance; B APHT/medical
  readiness; C implementation science.
- No production date, language, species, publication-type, or access-status filter
  was applied.
- The pre-execution audit found no exact A/B/C query in the workbook or repository.
  The earlier `search/README.md` assertion that the full strings resided in the
  workbook was inaccurate. The strings documented here are the initial
  prospective production freeze, not a reconstruction of an earlier search.
- Internal syntax and relevance-sample checks were performed. No formal PRESS
  peer review by an information specialist is claimed.

## Frozen strategies and execution

| Family | Strategy ID | UTC interval | Results | Exact query | Manifest |
|---|---|---:|---:|---|---|
| A — Core | `PUBMED-A-v1.0-2026-08-28` | 00:43:50–00:44:13 | 880 | `search/strategies/2026-08-28_pubmed_A_core.query.txt` | `search/exports/2026-08-28/2026-08-28_pubmed_A_core_manifest.json` |
| B — APHT | `PUBMED-B-v1.0-2026-08-28` | 00:44:13–00:44:28 | 391 | `search/strategies/2026-08-28_pubmed_B_apht.query.txt` | `search/exports/2026-08-28/2026-08-28_pubmed_B_apht_manifest.json` |
| C — Implementation | `PUBMED-C-v1.0-2026-08-28` | 00:44:28–00:44:43 | 194 | `search/strategies/2026-08-28_pubmed_C_implementation.query.txt` | `search/exports/2026-08-28/2026-08-28_pubmed_C_implementation_manifest.json` |

Each manifest records the complete reproducible PubMed URL, PubMed query
translation, filters/limits, exact timestamps, result count, export paths, and
SHA-256 values.

## Export reconciliation

| Family | Manifest count | ESearch count | NBIB PMID records | Hash verification |
|---|---:|---:|---:|---|
| A | 880 | 880 | 880 | PASS |
| B | 391 | 391 | 391 | PASS |
| C | 194 | 194 | 194 | PASS |

## Staging normalization and deduplication

- Records before cross-family deduplication: 1,465.
- Unique records: 1,456.
- Overlaps removed: 9, all by identical PMID.
- Overlap pattern: A+B=6; A+C=3; no B+C or A+B+C overlap.
- PMID present: 1,456/1,456.
- Normalized DOI present: 1,300/1,456.
- Fallback hierarchy: PMID, then normalized DOI, then normalized title+year.
- Deduplicated metadata SHA-256:
  `0433b363684aeca2dfc3ed76d79995c655bcdc27294f837837db716a698a3ab7`.
- Deduplicated RIS SHA-256:
  `f952ff56fa28bd67d36167aef334414f2687b8811277c3e4cb168f5825cf1dca`.

This is deterministic staging deduplication. It is not represented as the
required Zotero-native duplicate audit.

## Master Evidence audit

- Canonical rows: 1,456 (`EV-0001` through `EV-1456`).
- One unique PMID per row.
- Search provenance linked by strategy ID and provenance record ID.
- Titles present: 1,456/1,456, including three PubMed book records mapped from
  `BTI` rather than journal-article `TI`.
- Scientific workflow status: 1,456 `Identified`.
- Scientific traffic light: 1,456 caution/context.
- Transferability: 1,456 pending.
- Full text: 1,456 pending.
- Metadata verified: 0.
- Integrity/correction/retraction checked: 0.
- Claim-ready: 0.
- Every row states that identification metadata alone permits no substantive
  scientific, causal, operational, or institutional claim.
- `FXC7ZY9R` does not appear as an evidence record and is mentioned only in audit
  notes as the excluded controlled infrastructure test item.

## Workbook verification

- 14 sheets rendered and visually inspected.
- `MasterEvidenceTable`: `A3:EN1459` with 1,456 data rows.
- Formula ranges expanded through row 1459.
- Data validations and conditional formatting extended through row 1459.
- No `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, or `#N/A` found.
- XLSX ZIP package: valid.
- LibreOffice Calc: open/re-save PASS.
- Primary and LibreOffice-resaved copies: 14 sheets, 1,456 titles, 1,456 traffic
  lights, 1,456 transferability-pending formulas, and zero formula errors.
- Workbook SHA-256:
  `4734622037ad0ec66ee47d9c3a80a22bcf7ded6819c5a51ee91b7829f2b4fb13`.

## Zotero blocker

The historical Zotero release baseline remains PASS. This production run,
however, must import new records into the real Desktop library.

Observed in this environment:

- `profile: null`
- `prefs_file: null`
- `local_api_enabled_pref: null`
- `api_running: false`
- `connector_running: false`
- `selected-target`: connection refused
- authorized `import-ris --yes`: connection refused at `127.0.0.1:23119`

No production Zotero item key, collection assignment, tag assignment, duplicate
candidate, or merge result was invented.

## Risks and required next action

1. A and C intentionally favor sensitivity and include visible topical noise;
   title/abstract screening is required before relevance classification.
2. The search is structured for a conceptual essay and must not be reported as
   exhaustive systematic-review retrieval.
3. Formal PRESS review has not occurred.
4. DOI presence is not DOI verification; integrity/retraction checks remain open.
5. Military/combat evidence requires explicit transferability assessment and the
   project safety override before informing Brazilian institutional claims.

Exact next action: on the computer exposing the successful Zotero library and
`localhost:23119`, import
`search/exports/2026-08-28/2026-08-28_pubmed_ABC_deduplicated.ris`, place the
records in the planned project collections, run Zotero duplicate detection,
record candidate and merge counts, export the resulting library subset, and
map Zotero item keys back to the 1,456 Master Evidence rows. Only then may the
decision change from `PUBMED BLOCKED` to `PUBMED PASS`.
