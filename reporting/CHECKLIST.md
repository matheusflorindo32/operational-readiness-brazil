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
- [x] Export and bibliographic normalization
- [x] Zotero duplicate audit completed; controlled pair retained, no production merge

### PubMed A/B/C production execution — 2026-08-28
Historical status; see the 2026-09-05 structural audit below for current local controls.
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

### PubMed A/B/C production Zotero completion — 2026-09-03
**Status: GO for the completed infrastructure phase; `PUBMED PASS` is not
declared.** The literal 1,456-record Windows RIS was revalidated at SHA-256
`991c82352a8e94dbad7280aa98087dc928b30e356f5f5a436e7f61645d8c00b6`;
CRLF→LF normalization reproduced the canonical SHA-256
`f952ff56fa28bd67d36167aef334414f2687b8811277c3e4cb168f5825cf1dca`.
The production root `PE9UF4YN` now contains exactly 1,456 unique items, all
mapped one-to-one to `Master Evidence` and to the rollback manifest. Production
BibTeX and RIS exports each contain 1,456 records and exclude the controlled
item.

`FXC7ZY9R` retained its key, 32 tags, two notes, and two attachments and is
associated only with the separate top-level collection `EMHHKNTM`. The valid
Family A article PMID `37415704` was imported under production key `8XVBQIYE`.
Zotero's native duplicate view found exactly this intentional two-item group;
no merge was performed. Permanent decision: `DO NOT MERGE — controlled
infrastructure test versus production evidence`. Scientific screening remains
0/1,456. Overall checklist: 52/74 (70.3%); definitive evidence identification:
3/14 (21.4%). See `docs/ZOTERO_PUBMED_IMPORT_AUDIT_2026-09-03.md`.

Retry audit at `2026-08-28T17:10:33Z`: `status --json`, `probe`, `selected-target`,
`inventory`, `collections`, `tags`, and direct Connector ping were executed again.
No profile/library context or API route was available, so no write was attempted.
The 1,456-record RIS and its expected SHA-256 were reconfirmed. Percentages remain
unchanged and the gate remains `PUBMED BLOCKED`.

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

## Historical pre-analysis release status — 2026-09-06
**ZOTERO: 1,456 production + 1 controlled | PUBMED A/B/C: EXECUTED, IMPORTED AND RECONCILED | PRE-ANALYSIS CONTROLS: PASS | SCIENTIFIC SCREENING: NOT STARTED**

The earlier import BLOCKED status is superseded by the reconciled production
execution and current 44/44 structural controls. Operational PUBMED PASS becomes
effective only after the containing commit is confirmed remotely with successful
CI. See `docs/PUBMED_PREANALYSIS_GATE_2026-09-06.md` for evidence and limits.
OSF registration history is retained; independent public registration URL/DOI
verification remains pending. Overall administrative totals remain 52/74 (70.27%).

| Pre-analysis control (separate from the 74-item project checklist) | Evidence |
|---|---|
| Verified backup and stable identity map | 1,456/1,456; SQLite integrity ok |
| Coupled Claim-Ready, traffic light and Dashboard | 0/1,456 approvals |
| Imported retraction alert | PMID 26159007 retained and blocked |
| Stable IDs, integer scale, frozen headers, Analysis pending | Implemented in XLSX and Sheets |
| Functional tests | 24/24 per engine |
| Reconciliation and functional parity | 1,456/1,456 |
| Coherent documentation | README, checklist, changelog, report, rules and Drive index |
| Canonical Drive synchronization | Same ID, permissions preserved, backup retained |
| Remote publication and CI | Mandatory final gate; verify containing commit and CI run |

### PubMed structural publication audit — 2026-09-05
All 44 local controls passed: API/Connector HTTP 200; production 1,456;
controlled collection only FXC7ZY9R; library 1,457. Source RIS, manifest,
production RIS/BibTeX and Master Evidence reconcile one-to-one at 1,456/1,456.
Workbook baseline and Search Provenance corrections are complete; all other
workbook content and native features were preserved. No merges occurred.
The external backup passed hash, populated-schema and integrity checks.

The 156 source-missing DOIs, two same-title pairs with distinct PMIDs/years,
and generic Zotero document types are documented structural limitations.
Metadata verification is not individually complete. Scientific screening
remains 0/1,456. Checklist totals remain 52/74 (70.3%), identification 3/14.
`PUBMED PASS` additionally requires publication and successful CI for the exact
commit. See `docs/PUBMED_STRUCTURAL_AUDIT_2026-09-05.md`.

## Current controlled-screening status — 2026-09-07

**ZOTERO: UNCHANGED, 1,456 PRODUCTION + 1 CONTROLLED | PRIMARY TITLE/ABSTRACT SCREEN: 1,456/1,456 | HUMAN CONFIRMATION: 0/1,456 | CLAIM-READY: 0/1,456**

| Controlled-screening control | Result |
|---|---:|
| AI-assisted title/abstract classifications | 1,456/1,456 (100.00%) |
| Retained for full text | 1,206/1,456 (82.83%) |
| Proposed title/abstract exclusions | 9/1,456 (0.62%) |
| Pending human adjudication | 240/1,456 (16.48%) |
| Blocked by integrity | 1/1,456 (0.07%) |
| Priority union reviewed | 159/159 (100.00%) |
| Source-missing DOI absence reconfirmed | 156/156 (100.00%) |
| Missing DOI resolved | 0/156 (0.00%) |
| Metadata comparison without discrepancy | 1,366/1,456 (93.82%) |
| Identifier comparison without discrepancy | 1,454/1,456 (99.86%) |
| PubMed integrity fields checked | 1,456/1,456 (100.00%) |
| Human confirmations | 0/1,456 (0.00%) |
| Claim-Ready approvals | 0/1,456 (0.00%) |

The current PubMed EFetch record for PMID 26159007 identifies it as a retracted
publication and links retraction notice PMID 26357708. The row is retained,
marked `Not used`, and blocked from claims. Seventeen correction/update records
remain pending specific human review. Ninety metadata comparisons have an
explicit discrepancy (88 author-list representations, one journal/source and one
publication year); two source DOI values are absent from the current book-record
EFetch representation and remain pending. The two same-title groups remain four
separate records with `DO NOT MERGE`.

The local XLSX passed five rubric tests, structural parity, formula-error scan and
six negative workbook scenarios. A disposable native Google Sheets copy passed
the same row/count/identity/Claim-Ready checks and was deleted; the canonical
Sheet then reconciled to the XLSX at 1,456/1,456 with the same private owner-only
permission. Overall administrative progress remains 52/74 (70.27%); definitive
evidence identification remains 3/14 (21.43%). See
`docs/PUBMED_TITLE_ABSTRACT_SCREENING_2026-09-07.md`.
