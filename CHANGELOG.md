# Changelog

All notable project changes are documented here.

## [1.3.1] — 2026-09-05
### Audited and corrected
- Re-executed the Zotero skill's JSON status, inventory, collections and tags commands and reconciled the 1,456 production records against source RIS, rollback manifest, exports and Master Evidence.
- Corrected `README!B11` to the pre-execution baseline `912db0a4d3d6b9551fba228cd94d797b46370c50` and `Search Provenance!A2` to executed/imported/reconciled, screening not started. Preserved all other workbook content and native features.
- Recorded 156 source-missing DOIs, two title-only candidate pairs with distinct PMIDs/years, and the generic RIS/Zotero/BibTeX document-type mapping. Individual scientific metadata/integrity verification remains pending.
- Retained `DO NOT MERGE` for `FXC7ZY9R` / `8XVBQIYE`; rechecked live identity and membership against the preserved native audit.
- Verified the external SQLite backup by hash, integrity and populated schema. Excluded databases and private pre-import snapshots from version control.
- Added a reproducible read-only structural auditor and parser tests. Allowed only the two named production bibliographic exports through the 2 MB pre-commit size check.
- Full evidence and publication criteria: `docs/PUBMED_STRUCTURAL_AUDIT_2026-09-05.md`. No scientific screening started.

## [1.3.0] — 2026-09-03
### Executed
- Confirmed Zotero Desktop `10.0.1`, local API v3/schema 44, and API/Connector HTTP 200 through the installed Zotero skill.
- Preserved `FXC7ZY9R` with 32 tags, two notes, two attachments, and the same item key; associated it exclusively with top-level controlled collection `EMHHKNTM`.
- Imported the authorized 1,456-record PubMed A/B/C RIS into production root `PE9UF4YN` through Connector session `codex-operational-readiness-brazil-20260902T1515`.
- Executed Zotero's native duplicate view and found one candidate group: `FXC7ZY9R` versus production key `8XVBQIYE`. No merge was performed; permanent decision is `DO NOT MERGE — controlled infrastructure test versus production evidence`.

### Reconciled
- Reconciled 1,456 RIS records, 1,456 unique production Zotero items, 1,456 unique rollback-manifest keys, 1,456 BibTeX entries, 1,456 RIS-export records, and 1,456 `Master Evidence` rows.
- Mapped all `Master Evidence` rows to their real Zotero item keys with no missing rows, collisions, or use of `FXC7ZY9R`.
- Confirmed PMID `37415704` as production key `8XVBQIYE`, distinct from the controlled infrastructure key.
- Recorded both source hashes: Windows CRLF `991c82352a8e94dbad7280aa98087dc928b30e356f5f5a436e7f61645d8c00b6` and canonical LF `f952ff56fa28bd67d36167aef334414f2687b8811277c3e4cb168f5825cf1dca`.

### Verified
- Generated production-only BibTeX and RIS exports; each contains 1,456 records and excludes `FXC7ZY9R`.
- Updated the 14-sheet Evidence Command Center, scanned zero formula errors, validated the XLSX ZIP package, and visually reviewed every worksheet.
- Checklist advanced to 52/74 (70.3%); definitive evidence identification advanced to 3/14 (21.4%). Scientific screening remains 0/1,456.
- Decision for this infrastructure phase: **GO**. `PUBMED PASS` is not declared in this release.

## [1.2.1] — 2026-08-28
### Revalidated
- Re-ran the mandatory Zotero `status --json` pre-gate at `2026-08-28T17:10:33Z` from the session requested for production import.
- Confirmed `profile=null`, `prefs_file=null`, `api_running=false`, `connector_running=false`, and connection refusal at `127.0.0.1:23119`.
- Confirmed `selected-target`, inventory, collection, and tag routes were unavailable; no Zotero write was attempted after the failed pre-gate.
- Reconfirmed the combined RIS SHA-256 and exact 1,456-record count; `FXC7ZY9R` remains excluded from the production evidence set.
- Recorded the retry in the Evidence Command Center and revalidated all 14 sheets; updated workbook SHA-256: `67e5314e958de5a494ec1cd5cf7df09b58efa12d399038e463152b358da3f724`.
- Revalidated XLSX ZIP integrity and LibreOffice Calc open/re-save compatibility; the re-saved copy retained 14 sheets, `Master Evidence!A1:EN1459`, the retry audit block, and zero formula errors.
- Preserved all scientific counts and checklist percentages because the production Zotero gate did not advance.
- Decision remains **PUBMED BLOCKED**.

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
