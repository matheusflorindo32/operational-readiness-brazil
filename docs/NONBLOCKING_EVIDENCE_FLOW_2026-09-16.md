# Non-blocking controlled evidence progression — 2026-09-16

## Formal decision

**GO for controlled progression. Scientific PASS is not declared.**

The project can progress with independent clear records because all systemic
controls remained intact. Claim-Ready is 0/1,456, no human-review field was
populated, and no record is represented as scientifically approved.

## Entry state and preservation

- Remote and local entry commit: `dfdf5310319f9e3aeccf8798e2d1221aff7086b3`.
- PubMed production identities: 1,456/1,456.
- Canonical Master Evidence SHA-256 before/after:
  `2177618b04536e5a9c7b0feffe601b9847826b8fbb283715e2c071a1f604427b`.
- Zotero semantic inventory: identical before/after, 1,457 unique main items.
- Zotero API and Connector: HTTP 200; production root `PE9UF4YN`: 1,456;
  controlled collection `EMHHKNTM`: one item, `FXC7ZY9R`.
- No Zotero import, edit, merge, deletion or attachment operation occurred.
- `FXC7ZY9R` is absent from every generated scientific queue.

The raw PubMed refresh, Zotero JSON checks and source snapshots are retained in
the external dated backup tree and are not committed with personal Zotero data.

## Results by workstream

| Workstream | Result | Percentage | Operational effect |
|---|---:|---:|---|
| Reconciled identities | 1,456/1,456 | 100.00% | Systemic identity control passed |
| Integrity quarantine | 1/1,456 | 0.07% | Audit-only, never used |
| Current correction/update review | 18/1,456 | 1.24% | `REVIEW_REQUIRED` |
| Full-text candidates | 1,206/1,456 | 82.83% | Queue prepared |
| Active full-text queue | 1,191/1,206 | 98.76% | May progress to lawful discovery |
| Editorial hold within candidates | 15/1,206 | 1.24% | Outside use pending clarification |
| Direct PMC route identified | 393/1,206 | 32.59% | Lawful access route available |
| Access discovery required | 813/1,206 | 67.41% | Publisher/library discovery only |
| Pending adjudication | 240/1,456 | 16.48% | Preserved in 24 batches |
| Metadata differences documented | 90/90 | 100.00% | Source-preserving technical resolution |
| DOI representation conflicts resolved | 2/2 | 100.00% | Primary-source DOI confirmed |
| Human decisions added | 0 | 0.00% | Explicitly pending |
| Claim-Ready | 0/1,456 | 0.00% | Fail-closed |

### A. Retraction quarantine

[PMID 26159007](https://pubmed.ncbi.nlm.nih.gov/26159007/) remains in the
dataset only for audit and is marked `BLOCKED_INTEGRITY / NOT USED`. Its linked
[retraction notice](https://pubmed.ncbi.nlm.nih.gov/26357708/) remains the
primary integrity route. It cannot contribute to claims, synthesis or
conclusions.

### B. Editorial relations

The audited baseline contained 17 correction/update records. The current PubMed
refresh identified one additional relation for
[PMID 41997270](https://pubmed.ncbi.nlm.nih.gov/41997270/), linked to
[PMID 42728190](https://pubmed.ncbi.nlm.nih.gov/42728190/). Therefore the
current technical queue has 18 records. Fifteen belong to the 1,206 full-text
candidates and three belong to the 240 pending records. All are provisional
`REVIEW_REQUIRED`; no scientific impact was inferred from the relation type.

### C. Metadata and DOI resolution

The 90 historical metadata differences are fully represented in a ledger:
86 current PubMed authorship representations, one dual publication-date case,
and three earlier parser-representation cases. Both earlier DOI conflicts were
parser/representation effects in PubMed book records. The downstream DOI values
were confirmed as [10.17226/5257](https://doi.org/10.17226/5257) and
[10.17226/13380](https://doi.org/10.17226/13380) using PubMed/NCBI book records
and the DOI publisher routes. Previous values remain in the ledger; Zotero and
the canonical Master Evidence were not overwritten.

These are technical metadata resolutions. They do not verify article findings,
integrity beyond the recorded signals, eligibility after full text, or fitness
for a scientific claim.

### D. Full-text preparation

The 1,206 candidates received a transparent priority score based on lawful
access availability, operational relevance signals, potential design strength
and potential transferability. These scores order work only. They are not a
quality appraisal or risk-of-bias judgment. The active distribution is 793 P1,
383 P2 and 15 P3; a separate 15-record editorial hold remains outside active
use. Full-text obtained, quality appraisal, integrity cleared, human
confirmation and Claim-Ready all default to `NO` or pending.

### E. Pending adjudication

All 240 pending records remain unchanged and are divided into 24 batches of ten.
The queue preserves criterion, provisional AI status, confidence, source,
integrity state and the explicit boundary “what this article does not permit us
to claim.” Reviewer, date, decision and justification fields remain blank.

## Tests and regression controls

- Parser regression for PubMed book DOI, collective authors and collection title.
- Exact 1,456 identity cardinality and uniqueness.
- Exact queue partition: 1,206 candidates, 240 pending, nine proposed exclusions and one quarantine.
- Exact 18-record editorial queue and 90/90 plus 2/2 resolution ledgers.
- Zero `FXC7ZY9R` occurrences in generated queues.
- Zero populated human fields and zero Claim-Ready releases.
- Seven-sheet XLSX export, structural inspection and rendered summary review.
- Canonical Master Evidence SHA-256 unchanged.
- Zotero before/after semantic inventory identical; collection counts and controlled key rechecked live.

The generated control workbook SHA-256 is
`808985682db5bb553fd4709795e1066f9b62fdd8a8fd608e1ba2e004565ca082`.

## Artifacts

- Control workbook: `outputs/triage/2026-09-16/Operational_Readiness_Nonblocking_Queues.xlsx`.
- Machine-readable queues and manifest: `reporting/nonblocking/2026-09-16/`.
- Reproducible generator: `analysis/build_nonblocking_queues.py`.
- Regression tests: `analysis/test_nonblocking_queues.py` and existing screening/parser tests.

## Human work still required

Human adjudication remains required for the 18 correction/update records and
the 240 ambiguous title/abstract records. Every retained article still requires
lawful full-text review, compatible quality/risk-of-bias appraisal, integrity
review, exact source location and identified human confirmation before any
Claim-Ready release. No global scientific approval is permitted.
