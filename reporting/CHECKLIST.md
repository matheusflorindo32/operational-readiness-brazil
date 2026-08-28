# Project Checklist

## Protocol and conceptual design
- [x] Central title and tactical-athlete anchor retained
- [x] Paradigm-shift rationale defined
- [x] Primary question defined
- [x] Conceptual Essay Protocol v1.0 registered on OSF
- [x] Study design consolidated as conceptual and applied scientific essay
- [x] Structured and reproducible evidence-identification architecture retained
- [x] Three evidence families A/B/C retained
- [x] Ten database/platform environments prepared
- [x] Seed-set conceptual coverage pilot 15/15 documented
- [x] Transferability framework retained
- [x] CFIR + Proctor + ERIC implementation-science architecture retained
- [x] Major design correction documented in AMENDMENTS.md and CHANGELOG.md

## Infrastructure
- [x] GitHub repository created and materialized
- [x] README aligned with conceptual essay design
- [x] PROJECT_CHARTER aligned with conceptual essay design
- [x] PROTOCOL aligned with registered Conceptual Essay Protocol v1.0
- [x] AMENDMENTS updated
- [x] CHANGELOG updated
- [x] CITATION.cff updated
- [x] `.gitignore`, `.env.example`, pre-commit and SECURITY.md active
- [x] GitHub security workflow passed
- [x] Google Drive root folder created
- [x] Google Drive top-level structure created
- [x] OSF registration submitted/completed on 2026-08-26
- [x] OSF associated project recorded: https://osf.io/djgax
- [x] OSF registration materials: CC BY 4.0 International
- [x] Premium Elite Diamante evidence-workbook specification versioned in `docs/PREMIUM_ELITE_DIAMANTE_EVIDENCE_WORKBOOK_SPEC.md`
- [x] Premium Elite Diamante workbook implementation/export verified
- [ ] OSF public registration URL independently recorded in GitHub/workbook
- [ ] OSF DOI explicitly verified and recorded, if assigned

## Zotero Release Gate
- [x] Zotero skill instructions reviewed
- [x] `zotero/ZOTERO_COLLECTION_PLAN.md` verified as source of truth
- [x] Root collection name fixed: `Tactical Athlete → Operational Readiness Brazil`
- [x] Exactly 25 planned subcollections verified in the plan
- [x] Required tag taxonomy verified in the plan
- [x] Import/deduplication release-test protocol verified in the plan
- [x] Zotero Desktop local status executed with `status --json`
- [x] Local API on port 23119 verified
- [x] Initial inventory/collections/tags captured
- [x] Root collection created in Zotero Desktop
- [x] 25 subcollections materialized
- [x] Required tags materialized
- [x] Controlled RIS test set imported
- [x] DOI normalization verified
- [x] Duplicate detection verified
- [x] Controlled duplicate merge executed
- [x] Preservation of tags, notes and attachments verified
- [x] BibTeX export verified
- [x] RIS export verified
- [x] Zotero Desktop version and test timestamp recorded
- [x] `ZOTERO — PASS`

### Zotero execution attempt — 2026-08-26
**Status: BLOCKED in ChatGPT session.** The installed Zotero skill operates the user's local Zotero Desktop library through its localhost API (port 23119) from Codex. This ChatGPT session does not expose the user's local Zotero Desktop/localhost, so no real `status`, inventory, write, import, deduplication, merge, attachment-preservation, or export test was executed here. No result was fabricated. The Release Gate remains closed until the same test is executed in Codex on the computer running Zotero Desktop.

### Zotero execution attempt — 2026-08-27
**Status: BLOCKED after real command execution in the current Work Mode environment.** The required Zotero skill command `status --json` was executed. It returned `profile: null`, `prefs_file: null`, `local_api_enabled_pref: null`, `api_running: false`, `zotero_version: null`, `connector_running: false`, and connection refusal at `http://127.0.0.1:23119`. A controlled `enable --restart` attempt returned: `Could not find Zotero prefs.js. Start Zotero once, then retry.` Read-only `inventory --json`, `collections --json`, and `tags --json` each failed with connection refusal. No collection, tag, import, merge, attachment, or export result was fabricated. See `docs/EVIDENCE_COMMAND_CENTER_AUDIT_2026-08-27.md`.

### Zotero successful release-gate execution — 2026-08-27
**Status: PASS.** Executed on the computer running Zotero Desktop at
`2026-08-27T00:29:23-03:00`. Zotero Desktop `10.0.1`, local API v3/schema 44,
and Connector all responded successfully on `localhost:23119`. The initial
library inventory contained zero items, collections, and tags. The exact root
collection plus all 25 planned subcollections were then materialized and
verified through the local API. All 32 required tags were materialized on a
controlled real-metadata test record (PubMed PMID 37415704; DOI
`10.3389/fpubh.2023.1217187`).

Two controlled RIS imports produced duplicate candidates `FXC7ZY9R` and
`XLA6ZKCE`; a DOI supplied once with a `https://doi.org/` prefix normalized to
the canonical DOI. Zotero Desktop detected the duplicate pair and, after the
user's explicit confirmation, merged it into master item `FXC7ZY9R`. The master
was verified with all 32 tags, two notes, two stored text attachments, and a
`dc:replaces` relation to the merged duplicate. PubMed/NLM showed the item as a
Journal Article without a `CommentsCorrectionsList`, Crossref exposed no
`update-to`, `updated-by`, or relation entry, and the publisher article remained
available; no correction/retraction signal was found at the recorded check time.
BibTeX export produced one entry, and RIS export produced one record with the
canonical DOI, 32 tags, and both notes.

## Definitive structured evidence identification — RELEASED after Zotero gate PASS
- [x] PubMed A/B/C
- [ ] Scopus A/B/C
- [ ] Web of Science A/B/C
- [ ] SPORTDiscus A/B/C
- [ ] CINAHL A/B/C
- [ ] PsycINFO A/B/C
- [ ] Embase A/B/C
- [ ] Cochrane A/B/C
- [ ] SciELO A/B/C
- [ ] LILACS A/B/C
- [ ] Brazilian official/grey literature
- [ ] Citation chasing
- [ ] Export and bibliographic normalization
- [ ] Zotero deduplication

### PubMed A/B/C production execution — 2026-08-28
**Status: BLOCKED before PUBMED PASS.** The three final v1.0 queries were frozen
prospectively and executed through NCBI Entrez without date, language, species,
article-type, or access-status filters. Counts were A=880, B=391, and C=194.
NBIB and raw ESearch JSON exports reconcile exactly with those counts and their
recorded SHA-256 hashes. Deterministic staging normalization produced 1,456 unique
PMIDs after removal of nine cross-family overlaps; 1,300 records have normalized
DOIs. All 1,456 records were entered individually in `Master Evidence` as
`Identified`, with zero metadata-verified, integrity-checked, appraised, or
claim-ready records. Controlled test item `FXC7ZY9R` was not converted into an
evidence row.

The required production Zotero step could not be completed in this environment:
`status --json` returned no profile/prefs and `api_running=false`; `selected-target`
and the explicitly authorized `import-ris --yes` attempt both failed with connection
refusal at `127.0.0.1:23119`. The combined RIS is ready for the local Zotero run.
See `docs/PUBMED_ABC_AUDIT_2026-08-28.md`.

## Evidence synthesis and framework development
- [ ] Evidence map by operational-readiness domain
- [ ] Brazil × international evidence matrix
- [ ] Transferability assessment
- [ ] Implementation determinants/outcomes mapping
- [ ] Claim → source → result/page traceability
- [ ] Candidate framework domains assessed
- [ ] Proposed Brazilian Operational Readiness Framework derived
- [ ] Future empirical validation agenda defined
- [ ] Potential digital operational-readiness tool treated as a separate future validation phase

## Current release status
**OSF: COMPLETE | ZOTERO RELEASE BASELINE: PASS | PUBMED A/B/C: EXECUTED | MASTER EVIDENCE: 1,456 IDENTIFIED | PRODUCTION ZOTERO IMPORT/DEDUP: BLOCKED | PUBMED GATE: BLOCKED**
