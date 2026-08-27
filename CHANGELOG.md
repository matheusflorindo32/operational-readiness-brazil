# Changelog

All notable project changes are documented here.

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
