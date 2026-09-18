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

## Full-text evidence qualification pilot — 2026-09-17

**Decision: GO_NONBLOCKING_HUMAN_REVIEW_REQUIRED | HUMAN CONFIRMATION: 0/10 | CLAIM-READY: 0/1,456**

- [x] Entry commit, remote, CI, queues, hashes and prior invariants audited.
- [x] Zotero API/Connector HTTP 200; 1,457 main items; `PE9UF4YN` 1,456; `EMHHKNTM` only `FXC7ZY9R`.
- [x] First ten active P1 PMC records selected without editorial hold or integrity block.
- [x] Lawful full text obtained and hashed for 10/10.
- [x] PMID, DOI, PMCID and document identity matched for 10/10.
- [x] Article version recorded: 8/10 Version of Record and 2/10 Author Accepted Manuscript.
- [x] Current PubMed integrity check completed for 10/10 with bounded wording.
- [x] Design-specific AI-assisted appraisal completed for 10/10.
- [x] Extraction, exact location, supported/unsupported claims and transferability recorded for 10/10.
- [x] Red Team completed for 10/10 and commentary routed to `HUMAN_REVIEW_REQUIRED`.
- [x] Human reviewer/date/decision/justification/confirmation blank for 10/10.
- [x] `FXC7ZY9R` and PMID 26159007 absent from the pilot; quarantine preserved.
- [x] Regression suite passes 55/55.
- [ ] Identifiable human review completed — 0/10 (0.00%).
- [ ] Claim-Ready released — 0/10 (0.00%).

Pilot technical completion is 10/10 (100.00%). Provisional retention is 9/10
(90.00%); direct eligibility adjudication is 1/10 (10.00%); human confirmation
is 0/10 (0.00%). This is not scientific PASS.

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

## Gate 1 — documentary consistency — 2026-09-15

**Decision: PASS FOR GATE 1 ONLY | GATE 2 NOT STARTED | HUMAN SCIENTIFIC APPROVAL: 0/1,456**

- [x] GitHub `origin/main` and the clean checkout audited at the same starting commit.
- [x] Exact-commit CI audited as successful before modification.
- [x] README, checklist, changelog, current and historical reports compared.
- [x] Local XLSX and canonical Google Sheets reconciled at 10 red, 1,446 yellow and zero green.
- [x] Stale pre-analysis narrative corrected without changing data or decisions.
- [x] Master Evidence reconciled at 1,456 rows, unique Evidence IDs, PMIDs and production Zotero keys.
- [x] Claim-Ready and human-review fields remain 0/1,456.
- [x] Zotero API/Connector returned HTTP 200; `PE9UF4YN` has 1,456 items; `EMHHKNTM` contains only `FXC7ZY9R`; the library has 1,457 main items.
- [x] `FXC7ZY9R` remains isolated and `8XVBQIYE` remains the production key for PMID 37415704; `DO NOT MERGE` preserved.
- [x] Verified external pre-edit backup and SHA-256 manifest created.
- [x] Existing formula and screening regression controls re-executed; documentary regression added.
- [ ] Human adjudication of the 18 priority editorial-relation records — Gate 2, not started.

Gate 1 controls: 11/11 complete (100.00%). Current screening queues remain
1,206/1,456 retained (82.83%), 9/1,456 proposed exclusions (0.62%), 240/1,456
pending adjudication (16.48%) and 1/1,456 blocked by integrity (0.07%). Overall
administrative progress remains 52/74 (70.27%); definitive evidence
identification remains 3/14 (21.43%). See
`docs/GATE_1_DOCUMENTARY_CONSISTENCY_2026-09-15.md`.

## Gate 2 — preparation for human adjudication — 2026-09-15

**Decision: AGUARDANDO ADJUDICAÇÃO HUMANA | HUMAN DECISIONS: 0/18 | CLAIM-READY RELEASES: 0/18**

- [x] Gate 1 revalidated at the published commit and green CI.
- [x] Canonical XLSX and Google Sheets traffic light reconfirmed at 10 red, 1,446 yellow and zero green.
- [x] Priority queue reconciled at 18/18 unique PMIDs and 18/18 unique Zotero keys.
- [x] PMID 26159007 retained as the single retraction-priority record.
- [x] Seventeen correction/update relations rechecked through PubMed/NCBI EFetch.
- [x] Individual dossiers contain DOI, title, relation, primary URLs, AI-assisted decision, risk, rationale, claim limit and next action.
- [x] Human reviewer, date, decision and justification remain blank in 18/18 rows.
- [x] All 18 rows remain blocked from Claim-Ready; `FXC7ZY9R` is absent.
- [x] Local XLSX and separate native Google Sheet created with a controlled five-option decision field.
- [x] Zotero and canonical Master Evidence left unchanged; no import, merge or deletion occurred.
- [ ] Human adjudication completed — 0/18 (0.00%).

Gate 2 preparation controls: 10/10 complete (100.00%). Human adjudication is
0/18 (0.00%): one retraction record and 17 correction/update records await an
identified reviewer. Overall administrative progress remains 52/74 (70.27%);
definitive evidence identification remains 3/14 (21.43%). See
`docs/GATE_2_HUMAN_ADJUDICATION_PREPARATION_2026-09-15.md`.

## Gate 2 — high-rigor first cycle — 2026-09-15

**Decision: PILOT_READY | HUMAN ADJUDICATION: 0/18 | IMPORT: 0/18 | CLAIM-READY: 0/1,456**

- [x] Entry state revalidated: 10 red, 1,446 yellow and zero green.
- [x] Current PubMed source refreshed for PMID 26159007 and its retraction notice.
- [x] Assisted recommendation kept separate from the empty human decision.
- [x] Five pilot records selected across all required editorial and missing-identifier patterns.
- [x] Six dossiers contain source-specific facts and explicit `NOT VERIFIED` limits.
- [x] Missing DOI and missing notice PMID remain explicit; no identifier was inferred.
- [x] Fifteen fail-closed Gate 2 controls implemented and passing locally.
- [x] Zotero and Master Evidence verified unchanged in read-only comparisons.
- [x] No import, merge, reimport, deletion, Claim-Ready release or Gate 3 work.
- [ ] Identified human reviewer adjudicates PMID 26159007.
- [ ] Six complete human decisions pass intermediate pilot QC — 0/6 (0.00%).
- [ ] Remaining 12 records reviewed one at a time — 0/12 (0.00%).

Preparation for this cycle is 6/6 (100.00%). Human adjudication is 0/18
(0.00%); pilot adjudication is 0/6 (0.00%); import is 0/18 (0.00%); and
Claim-Ready is 0/1,456 (0.00%). See
`docs/GATE_2_FIRST_CYCLE_HIGH_RIGOR_2026-09-15.md`.

## Non-blocking controlled progression — 2026-09-16

**Decision: GO | CLAIM-READY: 0/1,456 | HUMAN DECISIONS ADDED: 0**

- [x] All 1,456 PubMed identities refreshed and reconciled without reimport.
- [x] Formal retraction retained for audit as `BLOCKED_INTEGRITY / NOT USED`.
- [x] Current correction/update queue built with 18 records: 17 audited baseline records plus one current delta.
- [x] All human reviewer, date, decision and justification fields left blank.
- [x] Historical metadata differences documented at 90/90 with previous and current primary values preserved.
- [x] Historical DOI representation conflicts resolved at 2/2 from PubMed/NCBI and DOI primary routes.
- [x] Full-text queue built for 1,206/1,206 candidates: 1,191 active and 15 on editorial hold.
- [x] Lawful-access route identified directly through PMC for 393/1,206 candidates; 813/1,206 remain discovery-required.
- [x] All 240 pending records retained in 24 reversible batches; three also carry `REVIEW_REQUIRED`.
- [x] Claim-Ready remains 0/1,456 and no quality/risk-of-bias appraisal is represented as complete.
- [x] Zotero postcheck passed: API/Connector HTTP 200, 1,457 main items, production root 1,456, controlled collection only `FXC7ZY9R`.
- [x] Zotero semantic inventory and canonical Master Evidence hash remained unchanged.
- [x] Reproducible CSV/JSON ledgers, XLSX control workbook and regression tests generated.

Operational controls are 13/13 complete (100.00%). The active full-text queue is
1,191/1,206 (98.76%); editorial hold is 15/1,206 (1.24%); pending adjudication
is 240/1,456 (16.48%); integrity quarantine is 1/1,456 (0.07%). This is a GO
for controlled progression, not scientific approval or PASS.

## XLSX artifact identity reconciliation — 2026-09-16

**Decision: GO_WITH_DOCUMENTED_NONSEMANTIC_VARIANCE | SCIENTIFIC PASS: PROHIBITED**

- [x] Both XLSX copies preserved read-only outside Git.
- [x] Binary hashes, sizes, origins, timestamps and Git blob recorded.
- [x] ZIP central directories and all OOXML member payloads compared.
- [x] Seven exact sheets, dimensions, values, types, formulas, hyperlinks, panes, tables, filters and validations compared.
- [x] Both copies received the same scientific semantic SHA-256.
- [x] All mandatory scientific invariants passed for both artifacts.
- [x] Human fields remain empty and Claim-Ready remains zero.
- [x] Root cause established as `ZIP_SERIALIZATION_DIFFERENCE`.
- [x] Deterministic semantic hash and fixed-input ZIP normalization implemented.
- [x] Save/reopen tests passed without Master Evidence change.
- [x] Formal incident report and machine-readable forensic evidence produced.

Artifact controls are 11/11 complete (100.00%). The canonical binary was not
replaced, Zotero was not modified and independent evidence work remains
`GO_NONBLOCKING`.

## Full-text Pilot 01 methodological correction — 2026-09-17

**Decision: GO_PILOT_02 | SCIENTIFIC PASS: PROHIBITED | HUMAN CONFIRMATION: 0/10 | CLAIM-READY: 0/1,456**

- [x] State and source commit `455dde313c9a2f81749189baf601334b733b0dbd` audited.
- [x] Original Pilot 01 artifacts and hashes preserved without overwrite.
- [x] MMAT EV-0787 expanded to S1/S2, 1.1–1.5, 4.1–4.5 and 5.1–5.5.
- [x] MMAT EV-0593 expanded to S1/S2, 1.1–1.5, 4.1–4.5 and 5.1–5.5.
- [x] Quantitative components classified as quantitative descriptive with reasons.
- [x] EV-0758 and EV-0523 reclassified and reappraised with current JBI Expert Opinion.
- [x] SANRA explicitly limited to narrative-review methodological-quality appraisal.
- [x] Methodological quality, risk of bias and textual-evidence appraisal separated.
- [x] Evidence classes and original-data/effect-estimate flags added for 10/10.
- [x] AI provisional completion separated from blank human confirmation.
- [x] EV-0787 and EV-0425 AAM/VOR status audited without erasing AAM identity.
- [x] EV-0523 remains non-empirical and `HUMAN_REVIEW_REQUIRED`.
- [x] Methodological Red Team passes 10/10 records and 130/130 checks.
- [x] Twelve named regressions plus preservation and Red Team controls pass.
- [x] Earlier regression suite preserved and passing.
- [x] Corrected XLSX reopened with seven sheets, exact summary values and zero formula-error matches.
- [x] Human fields blank and Claim-Ready zero.
- [ ] Identifiable human appraisal confirmation — 0/10 (0.00%).

Correction controls are 17/17 complete (100.00%). Appraisal architecture is
corrected for 10/10 records (100.00%); human confirmation is 0/10 (0.00%);
Claim-Ready is 0/10 (0.00%) and remains 0/1,456 globally. Pilot 02 processing
is zero records. `GO_PILOT_02` authorizes the next controlled batch only after
publication/CI and does not constitute scientific inclusion or PASS.

## Full-text Pilot 02 — 2026-09-17

**Decision: GO_PILOT_03 | SCIENTIFIC PASS: PROHIBITED | HUMAN CONFIRMATION: 0/10 | CLAIM-READY: 0/1,456**

- [x] Entry branch, local HEAD, `origin/main`, clean tree and exact-commit CI audited.
- [x] Canonical Master Evidence SHA-256 preserved.
- [x] First ten eligible `P1` PMC records selected deterministically with no Pilot 01 reuse.
- [x] Lawful full text and identity confirmed for 10/10.
- [x] Seven VOR and three AAM versions explicitly recorded.
- [x] Current PubMed integrity relations checked for 10/10 with dated limitations.
- [x] Four qualitative, two mixed-methods and four quasi-experimental designs classified.
- [x] Design-compatible appraisal completed provisionally for 10/10 and 110/110 domains.
- [x] MMAT mixed-methods coverage includes screening, qualitative, quantitative and integration criteria.
- [x] Extraction, exact locations, supported and unsupported claims, and transferability limits recorded for 10/10.
- [x] Red Team passed 10/10 record gates and 160/160 checks.
- [x] Human reviewer, date, decision, justification and confirmation blank in 10/10.
- [x] `FXC7ZY9R` and PMID 26159007 excluded from the batch.
- [x] Zotero, canonical Master Evidence and Pilot 01 artifacts preserved read-only.
- [x] Eight-sheet workbook, ledgers, source hashes and manifest generated.
- [x] Focused and repository regression suites passed before publication.
- [ ] Identifiable human confirmation — 0/10 (0.00%).
- [ ] VOR comparison for EV-1328 and EV-0791.
- [ ] VOR-specific evidence locations for all three AAM records.
- [ ] Claim-Ready release — 0/10 (0.00%).

Pilot 02 technical processing is 10/10 (100.00%). Cumulative processing is
20/1,191 active candidates (1.68%) and 20/383 active PMC-route candidates
(5.22%). Human confirmation is 0/20 across the two pilot queues and global
Claim-Ready remains 0/1,456. `GO_PILOT_03` authorizes only the next controlled
batch after publication and green CI.

## Full-text Pilot 03 — 2026-09-17

**Decision: GO_NEXT_BATCH | SCALE_READINESS: KEEP_BATCH_SIZE_10 | SCIENTIFIC PASS: PROHIBITED**

- [x] Entry HEAD, `origin/main`, clean checkout and exact-commit CI audited.
- [x] Master Evidence preserved at the same SHA-256 before/after.
- [x] Exactly ten next active `P1` PMC records selected with no Pilot 01/02 reuse.
- [x] Lawful full text and PMID/PMCID/DOI identity confirmed for 10/10.
- [x] Seven VOR and three AAM versions recorded; two full comparisons completed and one remains pending.
- [x] Current PubMed integrity check completed for 10/10 with bounded wording.
- [x] Designs and evidence classes confirmed before instrument selection.
- [x] Six appraisal routes applied and 95/95 provisional domains completed without global score.
- [x] Extraction, exact location, supported/unsupported claims and transferability recorded for 10/10.
- [x] Red Team passed 10/10 record gates and 230/230 controls.
- [x] Cumulative human queue contains 30 rows with all human fields blank.
- [x] `FXC7ZY9R` and PMID 26159007 remain excluded.
- [x] Pilot 02 derivative audited without replacing its canonical workbook.
- [x] Pilot 03 workbook, ledgers, hashes, builders and focused regressions generated.
- [ ] Identifiable human confirmation — 0/30 (0.00%).
- [ ] VOR comparison for EV-0252.
- [ ] Claim-level human source audit — 0/30 (0.00%).
- [ ] Claim-Ready release — 0/30 (0.00%); global 0/1,456.

Pilot 03 technical processing is 10/10 (100.00%). Cumulative technical progress
is 30/1,191 active candidates (2.52%) and 30/383 active PMC-route candidates
(7.83%). The next batch remains limited to ten records. No scientific PASS is
declared.
