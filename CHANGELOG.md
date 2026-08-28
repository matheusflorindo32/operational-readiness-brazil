# Changelog

All notable project changes are documented here.

## [1.2.0] — 2026-08-28
### Executed
- Audited the registered protocol and the existing search infrastructure before production execution.
- Identified and documented that the workbook provenance table contained no exact A/B/C strings despite the earlier README statement.
- Prospectively froze PubMed A/B/C v1.0 without date, language, species, article-type, or access-status filters.
- Executed real NCBI Entrez searches: A=880, B=391, C=194.
- Saved exact queries, raw ESearch JSON, NBIB exports, PubMed URLs, query translations, execution intervals, and SHA-256 checksums.

### Materialized
- Deterministically staged 1,456 unique PMIDs after removing nine cross-family PMID overlaps.
- Normalized 1,300 DOIs and generated a combined 1,456-record RIS for the required local Zotero import.
- Expanded `Master Evidence` from 500 to 1,456 records and retained one article/source per row (`EV-0001` through `EV-1456`).
- Classified every production row as `Identified`, caution/context, transferability pending, and not claim-ready.
- Preserved the controlled Zotero test item `FXC7ZY9R` solely as infrastructure evidence and excluded it from `Master Evidence`.

### Verified
- All family counts reconcile across manifests, ESearch JSON, and NBIB exports.
- All 14 workbook sheets passed visual inspection; validation and conditional-formatting ranges extend through row 1459.
- Formula-error scans returned zero `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, or `#N/A` errors.
- XLSX ZIP integrity passed; LibreOffice Calc opened and re-saved the workbook; both primary and re-saved copies re-imported with 14 sheets and 1,456 records.
- Final workbook SHA-256: `4734622037ad0ec66ee47d9c3a80a22bcf7ded6819c5a51ee91b7829f2b4fb13`.

### Release gate
- Overall checklist: 50/74 (67.6%).
- Definitive evidence-identification stage: 1/14 (7.1%).
- PubMed searches and workbook entry: complete.
- Production Zotero import/deduplication: **BLOCKED** because this environment cannot reach `localhost:23119`.
- Decision: **PUBMED BLOCKED**.

## [1.1.3] — 2026-08-27
### Audited and synchronized
- Independently audited commit `41ee5ac` against its parent `4f3e56b` and confirmed that the Zotero release-gate record is the only intervening commit.
- Reconciled the previously stale Evidence Command Center and audit report with the accepted `ZOTERO — PASS` execution record.
- Updated the workbook to 49/74 completed release items (66.2%), Zotero 21/21 (100%), definitive evidence identification 0/14 (released but not started), and decision `GO`.
- Preserved zero definitive evidence rows; controlled test item `FXC7ZY9R` remains explicitly excluded from scientific synthesis.
- Independently reconfirmed the test article's DOI, PMID, title, authorship, journal, year, and continued publisher/PubMed availability.

### Verified
- All 14 worksheets received a post-edit visual pass.
- Formula-error scans returned zero `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, or `#N/A` errors before and after export.
- XLSX ZIP-package integrity passed; LibreOffice Calc opened and re-saved the workbook successfully; both files re-imported with 14 sheets and the expected dashboard state.
- Final synchronized workbook SHA-256: `7e2a89c286ecfbb13d07ad68ac0f8a9675c35ff04eb9f20f0e8fcfd355bdfe64`.

### Release gate
- Zotero: **PASS**.
- Definitive structured evidence identification: **RELEASED**.
- Next-phase decision: **GO**.

## [1.1.2] — 2026-08-27
### Verified
- Passed the Zotero Desktop release gate on the computer exposing the real local API and Connector on `localhost:23119`.
- Materialized and verified the exact root collection, 25 subcollections, and 32 required tags.
- Verified controlled RIS import, DOI normalization, duplicate detection, user-confirmed duplicate merge, and preservation of tags, notes, and attachments.
- Verified one-record BibTeX and RIS exports for reproducibility.
- Recorded Zotero Desktop `10.0.1` and the successful test timestamp in `reporting/CHECKLIST.md`.

### Release gate
- Zotero: **PASS**.
- Definitive structured evidence identification: **RELEASED**.

## [1.1.1] — 2026-08-27
### Added
- Materialized the Premium Elite Diamante Evidence Command Center as a 14-sheet XLSX with a canonical 144-field `Master Evidence` table, 500 reserved evidence rows, dashboard, release-gate checklist, Zotero control, claim links, search provenance, quality/integrity, transferability, implementation-science, full-text, domain-coverage, and future-gap controls.
- Added formula-driven scientific traffic lights, DOI normalization, Brazil flag, transferability scoring/classification, claim-readiness control, record-completeness control, 43 data-validation rules, 18 conditional-formatting blocks, 10 structured tables, and 2 native charts.
- Added an independent workbook audit record in `docs/EVIDENCE_COMMAND_CENTER_AUDIT_2026-08-27.md`.

### Verified
- Formula-error scan returned no `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, or `#N/A` errors.
- A disposable in-memory formula test passed all expected outputs and was not saved to the workbook.
- Visual render review covered every worksheet; ZIP package integrity and LibreOffice open/re-save compatibility passed.
- The final workbook contains zero released definitive evidence records, as required while the Zotero gate is closed.

### Release gate
- Evidence Command Center: materialized and audited.
- Zotero: **BLOCKED** because the current environment cannot find `prefs.js` or a local Zotero profile and port 23119 refuses connection.
- Definitive structured evidence identification: **LOCKED**.

## [1.1.0] — 2026-08-26
### Changed
- Corrected the study design from a pre-registration JBI scoping-review framing to a **conceptual and applied scientific essay**.
- Reframed the A/B/C search architecture as **structured and reproducible evidence identification**, without claiming exhaustive systematic-review completeness.
- Removed JBI / PRISMA-ScR / PRISMA-S as governing study-design/reporting requirements for the essay.
- Preserved the 15-study seed-set pilot as a conceptual search-development artifact rather than an estimate of review sensitivity.
- Strengthened the paradigm-shift rationale for Brazilian public-safety personnel.
- Retained explicit transferability assessment for military/international tactical evidence.
- Retained CFIR, Proctor Implementation Outcomes, and ERIC as implementation-science supports rather than universal mandatory protocols.

### Registered
- Conceptual Essay Protocol v1.0 registered on OSF on 2026-08-26.
- OSF associated project: https://osf.io/djgax
- Registration materials use CC BY 4.0 International.
- OSF DOI will be added only after explicit verification.

### Release gate
- GitHub: complete.
- Google Drive: complete.
- OSF registration: complete.
- Zotero structure: pending.
- Definitive structured evidence identification: blocked until Zotero is materialized.

## [1.0.0] — 2026-08-25
### Added
- Frozen title, question, objective, PCC and initial eligibility criteria.
- Brazilian public-safety scope.
- Military/international transferability matrix.
- Grey-literature hierarchy.
- CFIR + Proctor + ERIC implementation architecture.
- Three-family evidence-identification architecture (Core / APHT / Implementation).
- Ten database/platform environments.
- Seed-set pilot covering 15/15 prespecified studies after architecture adjustments.
- PRESS-informed internal search audit.

### Historical status
The 2026-08-25 package used a scoping-review framing. That design was superseded before definitive evidence identification and is retained only as documented project history; see `AMENDMENTS.md` A-001.
