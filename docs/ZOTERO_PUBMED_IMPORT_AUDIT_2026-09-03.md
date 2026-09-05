# Zotero PubMed Production Import Audit — 2026-09-03

## Decision

Follow-up: the 2026-09-05 read-only structural audit passed all 44 local
controls and corrected the workbook baseline and Search Provenance text.
See `docs/PUBMED_STRUCTURAL_AUDIT_2026-09-05.md`. Counts and hashes below
describe the 2026-09-03 execution; the newer audit records the corrected
workbook hash. Publication/CI validation remains a separate commit-level check.

**GO for the completed Zotero infrastructure/import phase.** No duplicate merge
and no scientific screening were performed. `PUBMED PASS` is not declared.

## Environment and target

- Repository baseline: `912db0a4d3d6b9551fba228cd94d797b46370c50`.
- Zotero Desktop: `10.0.1`; local API v3/schema 44.
- Local API and Connector: HTTP 200 on `localhost:23119` at the preflight and
  resumption checks.
- Production root: `Tactical Athlete → Operational Readiness Brazil`, key
  `PE9UF4YN`.
- Controlled top-level collection: `Zotero Release Gate — Controlled Test — DO
  NOT USE`, key `EMHHKNTM`.
- The controlled collection already existed and was reused; no duplicate
  collection was created.

## Authorized input and byte-level validation

Input:
`search/exports/2026-08-28/2026-08-28_pubmed_ABC_deduplicated.ris`

- RIS records: 1,456.
- Literal Windows CRLF SHA-256:
  `991c82352a8e94dbad7280aa98087dc928b30e356f5f5a436e7f61645d8c00b6`.
- Canonical LF SHA-256:
  `f952ff56fa28bd67d36167aef334414f2687b8811277c3e4cb168f5825cf1dca`.
- Normalizing the local CRLF bytes to LF reproduced the canonical hash exactly.
- `.gitattributes` enforces LF for future `*.ris` and `*.bib` files.

## Backup and rollback protection

Before Zotero writes, a verified SQLite backup and inventory were created at:

`C:\Users\mathe\Documents\Codex\2026-08-26\zotero-plugin-zotero-openai-curated-remote\outputs\zotero-backups\2026-09-02T13-40-38-0300`

The SQLite backup passed `PRAGMA integrity_check` with `ok`. The repository
contains its backup manifest and a rollback manifest containing all 1,456 unique
production item keys. The controlled key `FXC7ZY9R` is absent from the rollback
manifest. No deletion or rollback was executed.

## Controlled item preservation

Before production import, `FXC7ZY9R` had 32 tags, two notes, two attachments,
four child objects, and no collection assignment. It was associated exclusively
with controlled collection `EMHHKNTM` without changing its bibliographic
metadata, key, tags, notes, or attachments.

Post-move audit:

- item key unchanged: `FXC7ZY9R`;
- collection membership exactly `[EMHHKNTM]`;
- tags: 32;
- notes: 2;
- attachments: 2;
- child keys: `SZNLEXCS`, `MSG5UCIN`, `2JGU6PBB`, `E4BKNKQ6`;
- absent from production root `PE9UF4YN` and all 25 planned subcollections;
- absent from `Master Evidence`, production exports, and rollback manifest.

The exclusion applies to the controlled **item key**, not to the PubMed article.

## Import execution and observability

- Connector session:
  `codex-operational-readiness-brazil-20260902T1515`.
- POST start: `2026-09-02T15:13:46.1827773-03:00`.
- Input submitted: the exact authorized 1,456-record RIS.

The long-running command session expired before its original Connector POST
HTTP status/body could be retained. Therefore this report does not invent or
reconstruct that response. Import completion is established independently by
the post-state: the library contains 1,457 top-level items, production root
`PE9UF4YN` contains 1,456 unique items, controlled collection `EMHHKNTM`
contains only `FXC7ZY9R`, and all 1,456 production keys reconcile to the source
and `Master Evidence`. Observed missing/failed production records: 0.

PMID `37415704` was imported as production key `8XVBQIYE`, which is distinct
from `FXC7ZY9R`. The Connector did not reuse the controlled key and did not
suppress the production article.

## Native duplicate audit

Zotero Desktop's native `Itens duplicados` view was opened after the import. It
reported exactly one two-item candidate group:

| Role | Item key | DOI | PMID | Collection | Distinguishing state |
|---|---|---|---|---|---|
| Controlled infrastructure test | `FXC7ZY9R` | `10.3389/fpubh.2023.1217187` | `37415704` | `EMHHKNTM` | 32 tags, 2 notes, 2 attachments; DOI-resolver URL; title without terminal period |
| Production Family A evidence | `8XVBQIYE` | `10.3389/fpubh.2023.1217187` | `37415704` | `PE9UF4YN` | `evidence-family:A`; PubMed URL; no child objects; title with terminal period |

No merge was performed. Permanent decision:
`DO NOT MERGE — controlled infrastructure test versus production evidence`.

Clarification from the live 2026-09-05 audit: the controlled item's PMID in
the table is a bibliographic crosswalk by DOI/title, not a stored Extra-field
PMID. The native-view result above is preserved historical evidence, not a
new native UI execution on 2026-09-05.

## Reconciliation

| Control surface | Expected | Observed | Result |
|---|---:|---:|---|
| Source RIS records | 1,456 | 1,456 | PASS |
| New production Zotero items | 1,456 | 1,456 unique | PASS |
| Rollback-manifest keys | 1,456 | 1,456 unique | PASS |
| Production BibTeX entries | 1,456 | 1,456 | PASS |
| Production RIS-export records | 1,456 | 1,456 | PASS |
| `Master Evidence` rows | 1,456 | 1,456 mapped to unique Zotero keys | PASS |
| Controlled additional item | 1 | `FXC7ZY9R` | PASS |
| Library top-level total | 1,457 | 1,457 | PASS |
| Scientific screening | 0 | 0 | PRESERVED |

Production exports:

- BibTeX SHA-256:
  `a4aec5f8dad0486f0d58106cd89e386b130463e23e19bd5f3a8c4f40a7d337a0`.
- RIS SHA-256:
  `57ad371bacd59a2df714afff635b11b55af20cef6225fcadabda503b7136e151`.
- Both exports exclude `FXC7ZY9R`.

The Evidence Command Center contains 14 worksheets, 1,456 mapped production
rows, no formula-error matches, and a valid XLSX ZIP package. Workbook SHA-256:
`dcebe8daf1e9038948e8a77bebe29b28b989e3a53f9c36b84f6cb7dca7d1d1a3`.

## Checklist and remaining risk

- Overall checklist: 52/74 (70.3%).
- Definitive evidence identification: 3/14 (21.4%).
- Zotero baseline: 21/21 (100%).
- Scientific screening: 0/1,456 (0%).
- Import failures after reconciliation: 0.
- Duplicate candidates awaiting no action in this round: one controlled pair.

Open risks and work intentionally not performed: scientific screening,
metadata/integrity verification of each source, transferability assessment,
non-PubMed database searches, and any future human-confirmed merge decision.
The retained Connector POST-response gap is an audit-trail limitation, but the
complete one-to-one post-state reconciliation supports the import count.

## Evidence artifacts

- `reporting/zotero-runs/2026-09-02T13-40-38-0300/09-status-2026-09-03.raw.txt`
- `reporting/zotero-runs/2026-09-02T13-40-38-0300/10-selected-target-2026-09-03.raw.txt`
- `reporting/zotero-runs/2026-09-02T13-40-38-0300/backup-manifest.json`
- `reporting/zotero-runs/2026-09-02T13-40-38-0300/rollback-manifest.json`
- `reporting/zotero-runs/2026-09-02T13-40-38-0300/08-controlled-item-after-move.json`
- `search/exports/2026-09-02/2026-09-02_pubmed_ABC_zotero_production.bib`
- `search/exports/2026-09-02/2026-09-02_pubmed_ABC_zotero_production.ris`
- `outputs/8a39e3c813da/PREMIUM_ELITE_DIAMANTE_Evidence_Command_Center.xlsx`
