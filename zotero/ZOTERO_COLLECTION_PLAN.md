# Zotero Collection Plan — Conceptual Essay Workflow

## Release-gate role
Zotero is the **bibliographic single source of truth** and the final infrastructure gate before definitive structured evidence identification begins.

## Root collection
**Tactical Athlete → Operational Readiness Brazil**

## Subcollections
1. Definitions / Concepts
2. Tactical Athlete
3. Human Performance
4. Operational Readiness
5. Law Enforcement
6. Military — Transferable Evidence
7. Firefighters
8. EMS / First Responders
9. APHT / TEMS / TCCC / TECC
10. Sleep / Fatigue / Recovery
11. Nutrition / Hydration
12. Cognition / Psychology
13. Injuries / Musculoskeletal
14. Cardiovascular / Cardiometabolic
15. External Load / Equipment
16. Wearables / Monitoring
17. Occupational Health / Longevity
18. Brazil
19. Implementation Science — CFIR / Proctor / ERIC
20. Frameworks / Guidelines / Consensus
21. Key Papers / Seed Studies
22. Official / Grey Literature
23. Core Evidence — Essay
24. Contextual / Supporting Evidence
25. Not Used / Out of Scope

## Required tags
### Status
- `status:seed`
- `status:core-evidence`
- `status:contextual`
- `status:not-used`
- `status:metadata-verified`
- `status:retraction-checked`

### Domain
- `domain:physical`
- `domain:occupational-performance`
- `domain:cognitive`
- `domain:recovery`
- `domain:health`
- `domain:load`
- `domain:injury`
- `domain:nutrition`
- `domain:apht`
- `domain:monitoring`
- `domain:implementation`
- `domain:longevity`

### Population / context
- `population:police`
- `population:firefighter`
- `population:first-responder`
- `population:military`
- `country:brazil`

### Transferability
- `transferability:high`
- `transferability:conditional`
- `transferability:low`

### Evidence role
- `role:definition`
- `role:framework`
- `role:indicator`
- `role:implementation`
- `role:brazil-context`
- `role:paradigm-shift`

## Rules
- Zotero is the bibliographic single source of truth.
- The workflow is for a **conceptual and applied scientific essay**, not systematic-review screening.
- Do not use `included/excluded` terminology as if a PRISMA screening process were being conducted.
- Verify DOI/PMID/metadata before an item receives `status:core-evidence`.
- Check corrections/retractions for core evidence before manuscript claims depend on the source.
- Store lawful personal-use full-text PDFs in Zotero/Drive, not GitHub.
- Use Zotero notes for brief claim/extraction pointers; the XLSX remains the structured evidence command center.
- Military evidence must receive an explicit transferability assessment before supporting Brazilian institutional recommendations.

## Import / deduplication release test
Before definitive evidence identification is released:
1. Create the root collection and all subcollections.
2. Confirm the collection inventory from Zotero Desktop/Codex.
3. Import a small test RIS/BibTeX set.
4. Verify DOI normalization and duplicate detection.
5. Confirm that duplicate merging preserves tags, notes, and attachments.
6. Confirm export to BibTeX/RIS for reproducibility.
7. Record the Zotero version and test date in the project checklist.

## Execution record — 2026-08-26
A Zotero Release Gate execution was requested from a ChatGPT session. The Zotero skill was reviewed, but the user's local Zotero Desktop API (`localhost:23119`) is not exposed to this session. Therefore no real Zotero status, inventory, collection/tag write, import, duplicate merge, attachment-preservation check, or export test was executed. The gate remains **BLOCKED** rather than being simulated.

The required next execution environment is **Codex on the computer running Zotero Desktop**, beginning with the skill's required `status --json` probe.

## Execution record — 2026-08-27
The Zotero Release Gate was executed successfully from Codex on the same
computer running Zotero Desktop. Zotero `10.0.1`, API v3/schema 44, and the
Connector responded on `localhost:23119`. The root collection and all 25 exact
subcollections were created and verified; all 32 planned tags were materialized.
A controlled two-record RIS test verified DOI normalization, Zotero duplicate
detection, and a user-confirmed duplicate merge. The merged master preserved all
32 tags, two notes, and two stored attachments. Real one-record BibTeX and RIS
exports were generated and validated. The test record's metadata matched PubMed
PMID 37415704 and DOI `10.3389/fpubh.2023.1217187`; PubMed/NLM, Crossref, and the
publisher page exposed no correction/retraction signal at the recorded check
time. Detailed evidence is recorded in `reporting/CHECKLIST.md`.

## Release condition
**Definitive structured evidence identification may begin only after the Zotero structure and import/deduplication test are verified.**

**Release condition satisfied on 2026-08-27: `ZOTERO — PASS`.**
