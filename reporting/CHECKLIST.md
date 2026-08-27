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
- [ ] Zotero Desktop local status executed with `status --json`
- [ ] Local API on port 23119 verified
- [ ] Initial inventory/collections/tags captured
- [ ] Root collection created in Zotero Desktop
- [ ] 25 subcollections materialized
- [ ] Required tags materialized
- [ ] Controlled RIS/BibTeX test set imported
- [ ] DOI normalization verified
- [ ] Duplicate detection verified
- [ ] Controlled duplicate merge executed
- [ ] Preservation of tags, notes and attachments verified
- [ ] BibTeX export verified
- [ ] RIS export verified
- [ ] Zotero Desktop version and test timestamp recorded
- [ ] `ZOTERO — PASS`

### Zotero execution attempt — 2026-08-26
**Status: BLOCKED in ChatGPT session.** The installed Zotero skill operates the user's local Zotero Desktop library through its localhost API (port 23119) from Codex. This ChatGPT session does not expose the user's local Zotero Desktop/localhost, so no real `status`, inventory, write, import, deduplication, merge, attachment-preservation, or export test was executed here. No result was fabricated. The Release Gate remains closed until the same test is executed in Codex on the computer running Zotero Desktop.

### Zotero execution attempt — 2026-08-27
**Status: BLOCKED after real command execution in the current Work Mode environment.** The required Zotero skill command `status --json` was executed. It returned `profile: null`, `prefs_file: null`, `local_api_enabled_pref: null`, `api_running: false`, `zotero_version: null`, `connector_running: false`, and connection refusal at `http://127.0.0.1:23119`. A controlled `enable --restart` attempt returned: `Could not find Zotero prefs.js. Start Zotero once, then retry.` Read-only `inventory --json`, `collections --json`, and `tags --json` each failed with connection refusal. No collection, tag, import, merge, attachment, or export result was fabricated. See `docs/EVIDENCE_COMMAND_CENTER_AUDIT_2026-08-27.md`.

## Definitive structured evidence identification — LOCKED until Zotero release gate passes
- [ ] PubMed A/B/C
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
**OSF: COMPLETE | EVIDENCE COMMAND CENTER: MATERIALIZED AND AUDITED | Zotero: BLOCKED — local Desktop profile/API execution required | DEFINITIVE EVIDENCE IDENTIFICATION: LOCKED**
